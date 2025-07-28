from django.db import models

# Create your models here.
from django.db import models
from users.models import CustomUser
from programs.models import Program
from counselling_session.models import Session

class Payment(models.Model):
    PAYMENT_STATUS = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    
    PAYMENT_METHODS = (
        ('stripe', 'Stripe'),
        ('paypal', 'PayPal'),
        ('mpesa', 'M-Pesa'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Optional references
    program = models.ForeignKey(Program, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(Session, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        return f"Payment #{self.id} - {self.amount} {self.currency} ({self.get_status_display()})"