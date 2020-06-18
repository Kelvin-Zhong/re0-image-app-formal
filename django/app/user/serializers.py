from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

from core.models import User
from core.user_model import LOGIN_TYPE_CHOICES, UserLoginType

from . import AUTH


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the users object"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'password', 'name')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user authentication object"""
    login_id = serializers.CharField()
    login_type = serializers.ChoiceField(
        choices=LOGIN_TYPE_CHOICES, default=UserLoginType.EMAIL)
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False,
        required=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        login_id = attrs.get('login_id')
        login_type = attrs.get('login_type')

        if login_type == UserLoginType.EMAIL:
            password = attrs.get('password')
            if not password:
                msg = 'User must provide password for email login'
                raise serializers.ValidationError(msg, code='authorization')
            
            user = authenticate(
                request=self.context.get('request'),
                username=login_id,
                password=password
            )

        if login_type == UserLoginType.WECHAT:
            # Step1: pass the login_id to wechat server to get openid
            js_code = login_id
            openid = AUTH.getOpenIDFromWechat(js_code)
            # Step2: check openid Django Database if it exists
            try: 
                user = User.objects.get(wechat_open_id=openid)
                print("found this user")
            except User.DoesNotExist:
                # Create a new user
                user = User.objects.create_wechat_user(
                    open_id=openid)
                print('finished creating the new user: ', user)

        if not user:
            msg = 'Unable to authenticate with provided credentials'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs