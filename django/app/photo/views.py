from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from core.authentication import ExpiringTokenAuthentication
from core.models import Photo
from core.photo_model import FacialExpressionType
from photo import serializers

from deeplearning.face_expression_detector import FaceExpressionDetector


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

        photo_data.facial_expression_type = label
        photo_data.save()
        photo_serializer = serializers.PhotoSerializer(photo_data)
        print("serializer data: ", photo_serializer.data)
        return Response(photo_serializer.data, status=status.HTTP_201_CREATED)
