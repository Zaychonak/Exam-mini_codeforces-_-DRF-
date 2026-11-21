from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    class Role(models.TextChoices):
        STUDENT = "student", "Student"
        ADMIN = "admin", "Admin"

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=16, choices=Role.choices, default=Role.STUDENT)

    def __str__(self):
        return self.username


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar_url = models.URLField(blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    organization = models.CharField(max_length=250, blank=True)
    about = models.TextField(blank=True)
    rating = models.IntegerField(default=0)
    max_rating = models.IntegerField(default=0)

    def __str__(self):
        return f"Profile {self.user.username}"






