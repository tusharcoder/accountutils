from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from .fields import SHA1Field
import hashlib


class ForgotPasswordModel(models.Model):
    """model for storing the reset password codes"""
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    code = SHA1Field()
        
        