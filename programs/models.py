from django.db import models

# Create your models here.
from django.db import models
from users.models import CustomUser

class Program(models.Model):
    TOPIC_CHOICES = (
        ('parenting', 'Parenting Excellence'),
        ('marriage', 'Marriage & Relationships'),
        ('addiction', 'Addiction Recovery'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    duration = models.PositiveIntegerField(default=6)  # Weeks
    topic = models.CharField(max_length=50, choices=TOPIC_CHOICES)
    counselor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, limit_choices_to={'user_type': 'counselor'})
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title

class ProgramEnrollment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    enrollment_date = models.DateTimeField(auto_now_add=True)
    progress = models.PositiveIntegerField(default=0)  # Percentage
    completed = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'program')
    
    def __str__(self):
        return f"{self.user.username} - {self.program.title}"

class Resource(models.Model):
    RESOURCE_TYPES = (
        ('pdf', 'PDF'),
        ('video', 'Video'),
        ('worksheet', 'Worksheet'),
        ('audio', 'Audio'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPES)
    file_url = models.URLField()
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    session = models.ForeignKey('sessions.Session', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title