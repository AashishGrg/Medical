from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Create and save a user with the given email, and password.
        """

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)


class PortalUser(AbstractUser):
    USER_TYPES = (
        ('patient', 'patient'),
        ('doctor', 'doctor'),
        ('examiner', 'examiner'),
    )
    username = None
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=16)
    address = models.CharField(max_length=64)
    user_type = models.CharField(choices=USER_TYPES, max_length=64)
    is_verified = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='media/images/user/')
    objects = UserManager()
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email


class DoctorSpeciality(models.Model):
    name = models.CharField(max_length=64, unique=True)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(PortalUser, on_delete=models.CASCADE, related_name='spec_creater')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    liscence_id = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(PortalUser, on_delete=models.CASCADE, related_name='doctor')
    speciality = models.ManyToManyField(DoctorSpeciality, related_name='doc_speciality')
    is_active = models.BooleanField(default=False)
    liscence_file = models.FileField(upload_to='media/images/doctor/liscence/')
    is_verified = models.BooleanField(default=False)
    degree = models.CharField(max_length=128)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Patient(models.Model):
    user = models.ForeignKey(PortalUser, on_delete=models.CASCADE, related_name='patient')
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.email


class Examiner(models.Model):
    liscence_id = models.CharField(max_length=32, unique=True)
    user = models.ForeignKey(PortalUser, on_delete=models.CASCADE, related_name='examiner')
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    degree = models.CharField(max_length=128)

    def __str__(self):
        return self.user.email
