from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils import timezone

from apps.account import managers as account_manager


class User(AbstractUser):
    CLIENT = 'client'
    DRIVER = 'driver'

    USER_TYPES = (
        (CLIENT, "Client", ),
        (DRIVER, "Driver", ),
    )
    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    username_validator = UnicodeUsernameValidator()
    dob = models.DateField(null=True)
    phone = models.CharField(max_length=60, null=True, unique=True)
    username = models.CharField(
        'username',
        max_length=150,
        unique=True,
        help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.',
        validators=[username_validator],
        error_messages={
            'unique': "A user with that username already exists.",
        },
    )
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True, null=True)
    user_type = models.CharField(max_length=60, choices=USER_TYPES)

    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.',
    )
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = account_manager.UserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()


class DriverProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='drivers')
    car_number = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return '{}, driver - {}'.format(self.user.get_full_name(), self.car_number)


class ClientProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients')

    def __str__(self):
        return '{}, client'.format(self.user.get_full_name())
