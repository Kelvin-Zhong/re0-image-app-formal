from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.authentication import ExpiringTokenAuthentication
from core.models import Photo
from core.photo_model import FacialExpressionType
from photo import serializers

from deeplearning.face_expression_detector import FaceExpressionDetector

from io import BytesIO

from django.core.files.base import ContentFile

from PIL import Image, ImageDraw, ImageFont

FONT_PATH = 'photo/arial.ttf'


def addTextToImg(img, text):
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype(FONT_PATH, size=45)
    color = 'rgb(255, 255, 255)'  # white color
    text_coordinates = (50, 50)
    draw.text(text_coordinates, text, fill=color, font=font)
    return img


def saveImageToContentFile(img):
    img_io = BytesIO()
    img.save(img_io, format='png', quality=100)
    img_content = ContentFile(img_io.getvalue())
    return img_content


class PhotoViewSet(viewsets.ModelViewSet):
    """Manage photo related API"""
    serializer_class = serializers.PhotoSerializer
    queryset = Photo.objects.all()
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset.filter(user=self.request.user)
        if self.action == 'list':
            queryset = queryset.order_by('created_time')[:20]
        return queryset

    def perform_create(self, serializer):
        """Creation behavior of the user"""
        serializer.save(user=self.request.user)
    
    def create(self, request):
        serializer = serializers.PhotoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

        photo_data = serializer.save(user=self.request.user)

        img_path = photo_data.image.path
        detector = FaceExpressionDetector(img_path)
        label = detector.run()
        if label == 1:
            # label = 'happy'
            label = FacialExpressionType.HAPPY
        else:
            # label = 'unhappy'
            label = FacialExpressionType.UNHAPPY
        print("Predicted Label: ", label)

        # Add label as text to image
        img = Image.open(img_path)
        img = addTextToImg(img, label)

        # Save image to photo model
        content_file = saveImageToContentFile(img)
        photo_data.image.save(photo_data.image.name, content_file)

        photo_data.facial_expression_type = label
        photo_data.save()
        photo_serializer = serializers.PhotoSerializer(photo_data)
        print("serializer data: ", photo_serializer.data)
        return Response(photo_serializer.data, status=status.HTTP_201_CREATED)
