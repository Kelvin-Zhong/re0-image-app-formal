from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from core.authentication import ExpiringTokenAuthentication
from core.models import Photo
from photo import serializers


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
