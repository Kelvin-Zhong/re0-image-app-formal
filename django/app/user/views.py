from rest_framework import generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from user.serializers import UserSerializer, AuthTokenSerializer

from core import models
from core.authentication import token_expire_handler, \
    ExpiringTokenAuthentication


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the autheticated user"""
    serializer_class = UserSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """Retrieve and return authed user"""
        return self.request.user


class ListUserView(generics.ListAPIView):
    """List all the users in the system"""
    serializer_class = UserSerializer
    queryset = models.User.objects.all()


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for the user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        is_expired, token, token_expired_timestamp = token_expire_handler(
            token)
        return Response({
            'user_id': user.id,
            'token': token.key,
            'token_expired_timestamp': token_expired_timestamp})
