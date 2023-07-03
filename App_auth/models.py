import re
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):
    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError("The username field must be set!")

        if re.match(r'^[a-zA-Z0-9.!#$%&\'*+/=?^_`{|}~-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*$',
                    username):
            username = self.normalize_email(username)
        else:
            phone_regex = r'^\+?880\d{10}$'
            phone_validator = RegexValidator(
                regex=phone_regex,
                message="Enter a valid Bangladeshi phone number."
            )
            phone_validator(username)

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True")

        return self._create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.id and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super(CustomUser, self).save(*args, **kwargs)


class AdminProfileModel(models.Model):
    GENDER_OPTION = (
        ('M', 'M'),
        ('F', 'F'),
        ('O', 'O'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_query_name="admin_profile")
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_OPTION)
    phone_regex = RegexValidator(
        regex=r'^\+?880\d{10}$',
        message="Phone number must be entered in the format: '+880xxxxxxxxxx'."
    )
    phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=15)

    def __str__(self):
        return self.full_name


class ResearcherProfileModel(models.Model):
    GENDER_OPTION = (
        ('M', 'M'),
        ('F', 'F'),
        ('O', 'O'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_query_name="researcher_profile")
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_OPTION)
    phone_regex = RegexValidator(
        regex=r'^\+?880\d{10}$',
        message="Phone number must be entered in the format: '+880xxxxxxxxxx'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    institute = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class ReaderProfileModel(models.Model):
    GENDER_OPTION = (
        ('M', 'M'),
        ('F', 'F'),
        ('O', 'O'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_query_name="reader_profile")
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_OPTION)
    phone_regex = RegexValidator(
        regex=r'^\+?880\d{10}$',
        message="Phone number must be entered in the format: '+880xxxxxxxxxx'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    institute = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class ReviewerProfileModel(models.Model):
    GENDER_OPTION = (
        ('M', 'M'),
        ('F', 'F'),
        ('O', 'O'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_query_name="reviewer_profile")
    full_name = models.CharField(max_length=255)
    gender = models.CharField(max_length=1, choices=GENDER_OPTION)
    phone_regex = RegexValidator(
        regex=r'^\+?880\d{10}$',
        message="Phone number must be entered in the format: '+880xxxxxxxxxx'."
    )
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    institute = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name
