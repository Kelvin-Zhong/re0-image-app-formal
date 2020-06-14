from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import AuthenticationFailed

import time
from datetime import timedelta
from django.utils import timezone
from django.conf import settings


# if token is expired, it be will replaced by the new token
# and new one with different key will be created
def token_expire_handler(token):
    time_elapsed = timezone.now() - token.created
    left_time = timedelta(
        seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed

    is_expired = left_time < timedelta(seconds=0)
    if is_expired:
        token.delete()
        token = Token.objects.create(user=token.user)

    token_expired_time = token.created + \
        timedelta(seconds=settings.TOKEN_EXPIRED_AFTER_SECONDS)
    token_expired_timestamp = int(
        time.mktime(token_expired_time.timetuple()))
    return is_expired, token, token_expired_timestamp


class ExpiringTokenAuthentication(TokenAuthentication):
    """
    If token is expired then it will be removed
    and new one with different key will be created
    """

    def authenticate_credentials(self, key):
        try:
            token = Token.objects.get(key=key)
        except Token.DoesNotExist:
            raise AuthenticationFailed("Invalid Token")

        if not token.user.is_active:
            raise AuthenticationFailed("User is not active")

        is_expired, token, token_expired_timestamp = token_expire_handler(
            token)
        if is_expired:
            raise AuthenticationFailed("The Token is expired")
        return (token.user, token)