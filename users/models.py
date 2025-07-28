# from django.db import models

# # Create your models here.
# from django.db import models
# from django.contrib.auth.models import AbstractUser

# class CustomUser(AbstractUser):
#     USER_TYPES = (
#         ('client', 'Client'),
#         ('couple', 'Couple'),
#         ('counselor', 'Counselor'),
#         ('admin', 'Administrator'),
#     )
    
#     user_type = models.CharField(max_length=20, choices=USER_TYPES, default='client')
#     phone = models.CharField(max_length=20, blank=True)
#     is_anonymous = models.BooleanField(default=False)
#     alias = models.CharField(max_length=100, blank=True)  # For anonymous users
#     subscription_status = models.CharField(max_length=20, default='inactive')
#     created_at = models.DateTimeField(auto_now_add=True)
    
#     def __str__(self):
#         return f"{self.username} ({self.get_user_type_display()})"

# class UserProfile(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
#     bio = models.TextField(blank=True)
#     specialization = models.CharField(max_length=100, blank=True)  # For counselors
#     profile_picture = models.URLField(blank=True)
#     topics = models.JSONField(default=list)  # ['Parenting', 'Marriage', etc.]
    
#     def __str__(self):
#         return f"Profile of {self.user.username}"

from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('client', 'Client'),
        ('couple', 'Couple'),
        ('counselor', 'Counselor'),
        ('admin', 'Administrator'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='client')
    phone = models.CharField(max_length=20, blank=True)
    is_anonymous = models.BooleanField(default=False)
    alias = models.CharField(max_length=100, blank=True)  # For anonymous users
    subscription_status = models.CharField(max_length=20, default='inactive')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add these overrides to fix the reverse accessor clash
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name="customuser_set",  # Unique reverse name
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="customuser_set",  # Unique reverse name
        related_query_name="user",
    )
    
    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    specialization = models.CharField(max_length=100, blank=True)  # For counselors
    profile_picture = models.URLField(blank=True)
    topics = models.JSONField(default=list)  # ['Parenting', 'Marriage', etc.]
    
    def __str__(self):
        return f"Profile of {self.user.username}"