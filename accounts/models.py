from django.db import models
from django.contrib.auth.models import User
from encrypted_model_fields.fields import EncryptedCharField

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    encrypted_info = EncryptedCharField(max_length=100)  # Example encrypted field
    #Campos para recuperacion OTP
    reset_otp = models.CharField(max_length=4, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)
