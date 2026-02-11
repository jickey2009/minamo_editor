from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from . import models
# Register your models here.

admin.site.register(CustomUser, UserAdmin)
admin.site.register(models.Book)
admin.site.register(models.Chapter)
admin.site.register(models.Section)