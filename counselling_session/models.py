from django.db import models

# Create your models here.
from django.db import models
from users.models import CustomUser
from programs.models import Program

class Session(models.Model):
    SESSION_TYPES = (
        ('live', 'Live Session'),
        ('recorded', 'Recorded Session'),
    )
    
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    session_type = models.CharField(max_length=20, choices=SESSION_TYPES, default='live')
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    counselor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name='sessions_conducted')
    scheduled_time = models.DateTimeField()
    duration = models.PositiveIntegerField()  # Minutes
    google_meet_link = models.URLField(blank=True)
    recording_url = models.URLField(blank=True)
    is_available = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.title} ({self.get_session_type_display()})"

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    booked_at = models.DateTimeField(auto_now_add=True)
    attended = models.BooleanField(default=False)
    feedback_provided = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('user', 'session')
    
    def __str__(self):
        return f"{self.user.username} - {self.session.title}"

class Feedback(models.Model):
    RATING_CHOICES = (
        (1, 'Poor'),
        (2, 'Fair'),
        (3, 'Good'),
        (4, 'Very Good'),
        (5, 'Excellent'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'session')
    
    def __str__(self):
        return f"Feedback for {self.session.title} by {self.user.username}"