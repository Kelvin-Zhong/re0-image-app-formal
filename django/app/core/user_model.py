from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


LOGIN_TYPE_CHOICES = [
    ['EMAIL', 'EMAIL'],
    ['WECHAT', 'WECHAT'],
]


class UserLoginType(object):
    EMAIL = 'EMAIL'
    WECHAT = 'WECHAT'


class UserManagerBase(BaseUserManager):
    """UserManager doc"""

    def create_email_user(self, email, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            login_id=email,
            login_type=UserLoginType.EMAIL,
            email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_wechat_user(self, open_id, **extra_fields):
        """Function specific for creating wechat users"""
        name = 'test user'
        user = self.model(
            login_id=open_id,
            login_type=UserLoginType.WECHAT,
            wechat_open_id=open_id,
            name=name,
            **extra_fields)
        # Empty password for wechat login
        user.set_unusable_password()

        # Save it to database
        user.save(using=self._db)
        return user

    def create_user(self, login_id, login_type, password=None, **extra_fields):
        """Creates and saves a new User"""
        if not login_id or not login_type:
            raise ValueError('Users must have an login_id and login_type')
            
        if login_type == UserLoginType.EMAIL:
            return self.create_email_user(
                login_id,
                password,
                **extra_fields)
        else:
            return self.create_wechat_user(open_id=login_id, **extra_fields)
            
    def create_superuser(self, login_id, login_type, password):
        """Creates and saves a new super user"""
        if login_type != UserLoginType.EMAIL:
            raise ValueError('Super user always need email login')

        user = self.create_user(
            login_id=login_id,
            login_type=login_type,
            password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserBase(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    email = models.EmailField(max_length=255, default='')
    wechat_open_id = models.CharField(max_length=255, default='')
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    login_id = models.CharField(max_length=255, unique=True)
    login_type = models.CharField(
        max_length=255,
        choices=LOGIN_TYPE_CHOICES,
        default=UserLoginType.EMAIL)

    objects = UserManagerBase()

    # USERNAME_FIELD = 'email'
    USERNAME_FIELD = 'login_id'
    REQUIRED_FIELDS = ['login_type']
