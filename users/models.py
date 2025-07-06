from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        user = self.create_user(email, password, **extra_fields)

        Profile.objects.create(user=user, role='admin')

        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username


class Profile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('veteran', 'Veteran'),
        ('newbie', 'Newbie'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='newbie')
    avatar = models.ImageField(upload_to='avatars', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    github = models.URLField(blank=True)
    telegram = models.URLField(blank=True)
    youtube = models.URLField(blank=True)
    linkedin = models.URLField(blank=True)
    is_online = models.BooleanField(default=False)

    def get_role_color_class(self):
        return {
            'admin': 'bg-red-600',
            'veteran': 'bg-amber-600',
            'newbie': 'bg-green-600',
        }.get(self.role, 'bg-gray-400')

    def __str__(self):
        return f"{self.user.username} Profile"
