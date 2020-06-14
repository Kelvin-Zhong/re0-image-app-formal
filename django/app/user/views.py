from rest_framework import generics, permissions

from user.serializers import UserSerializer

from core import models


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the autheticated user"""
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authed user"""
        return self.request.user


class ListUserView(generics.ListAPIView):
    """List all the users in the system"""
    serializer_class = UserSerializer
    queryset = models.User.objects.all()