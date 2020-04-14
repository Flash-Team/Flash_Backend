from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, User
from django.db import models
from django.utils import timezone


class MyAbstractUser(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=False)
    last_name = models.CharField(max_length=30, blank=False)
    email = models.EmailField(blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    phone_number = models.CharField(max_length=11)

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        abstract = True

    @property
    def full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()


class MyUser(MyAbstractUser):

    USER_ROLES = (
        (1, 'Admin'),
        (2, 'Manager'),
        (3, 'Client'),
        (4, 'Courier')
    )

    role = models.IntegerField(choices=USER_ROLES, default=3)

    @property
    def undone_orders(self):
        return self.orders.filter(delivered=False)

    @property
    def done_orders(self):
        return self.orders.filter(delivered=False)

    @classmethod
    def save_user(cls, data, password):
        user = cls.objects.create_user(**data)

        user.set_password(password)

        user.save()

        return user

    def __str__(self):
        return '{} [username: {}, phone: {}, role: {}]'\
            .format(self.full_name, self.username, self.phone_number, self.role)
