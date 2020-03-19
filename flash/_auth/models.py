from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager

class MyAbstractUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        abstract = True

class MyUser(MyAbstractUser):
        USER_ROLES = (
            (1, 'Admin'),
            (2, 'Manager'),
            (3, 'Client'),
            (4, 'Courier')
        )
        role = models.IntegerField(choices=USER_ROLES, default=3)

        def set_user_role(self, value):
            self.role = value
