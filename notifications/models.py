from django.db import models

# Create your models here.
from django.db import models
from django.utils import timezone
from users.models import CustomUser
from programs.models import Program
from counselling_session.models import Session

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('push', 'Push Notification'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    message = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now)
    read = models.BooleanField(default=False)
    
    # Optional references
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_notification_type_display()} to {self.user.username}"