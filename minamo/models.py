from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
# Create your models here.

class CustomUser(AbstractUser):
    pass

class Book(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    length = models.IntegerField(default=0)
    next_chapter_order = models.IntegerField(default=1)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return self.title
    
class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    length = models.IntegerField(default=0)
    next_section_order = models.IntegerField(default=1)
    order = models.IntegerField()
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.book.title} - {self.title}"
    
class Section(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, default="New Section")
    content = models.TextField()
    content_head = models.CharField(max_length=200, blank=True)
    order = models.IntegerField()
    length = models.IntegerField(default=0)
    created_date = models.DateField(default=timezone.now)
    updated_date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.chapter.title} - Section {self.order}"
    
class Configuration(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    dark_mode = models.BooleanField(default=False)
    UD_Digi = models.BooleanField(default=False)
    text_size = models.IntegerField(default=14)
    textarea_height = models.IntegerField(default=20)
    textarea_width = models.IntegerField(default=40)
    text_vertical_align = models.BooleanField(default=False)

    def __str__(self):
        return f"Configuration for {self.user.username}"