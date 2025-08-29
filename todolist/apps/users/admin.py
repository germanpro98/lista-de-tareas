from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser  # o como se llame tu modelo

admin.site.register(CustomUser, UserAdmin)