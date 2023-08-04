from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
# Create your models here.

class Publisher(models.Model):
    publisher_name = models.CharField(max_length=255)
    publisher_phone = models.CharField(max_length=255)
    publisher_adress = models.CharField(max_length=255)

class Category(models.Model):
    category = models.CharField(max_length=255, blank=True)

class Book(models.Model):
    book_name = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    give_back = models.BooleanField(blank=False, default=True)
    book_category = models.ForeignKey(Category, on_delete=models.CASCADE, blank=True, null=True)

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True)
    return_state = models.BooleanField(blank=False, default=False)
    return_state_request = models.BooleanField(blank=False, default=False)
    borrow_time = models.DateField(default=timezone.now)