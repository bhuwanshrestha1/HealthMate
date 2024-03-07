from django.contrib import admin

from .models import CustomUser
from .models import Doctor

admin.site.register(CustomUser)
admin.site.register(Doctor)