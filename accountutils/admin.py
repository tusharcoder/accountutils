from django.contrib import admin

# Register your models here.
from .models import ForgotPasswordModel

admin.site.register(ForgotPasswordModel)