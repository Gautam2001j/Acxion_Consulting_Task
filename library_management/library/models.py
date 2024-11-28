from email.policy import default
from random import choices
from secrets import choice

from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group, Permission


class CustomUser(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name="customuser_set",  # Use a unique related_name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="customuser_permissions_set",  # Use a unique related_name
        blank=True
    )

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    serial_number = models.CharField(max_length=100, unique=True)
    is_available = models.BooleanField(default=True)


class Membership(models.Model):
    first_name = models.CharField(max_length=50, default="DefaultString")
    last_name = models.CharField(max_length=50, default="DefaultString")
    contact_name = models.CharField(max_length=100, default="DefaultString")
    contact_address = models.TextField(null=True, blank=True)
    aadhar_card_number = models.CharField(max_length=12, default='000000000000')
    start_date = models.DateField()
    end_date = models.DateField()
    type_choices = (('6-months','6 Months'),('1-year','1 Year'),('2-year','2 Year'))
    membership_duration = models.CharField(max_length=20, choices=type_choices, default="DefaultString")

class BookMovie(models.Model):
    TYPE_CHOICES = (('book', 'Book'), ('movie', 'Movie'))
    book_or_movie = models.CharField(max_length=10, choices=TYPE_CHOICES)
    name = models.CharField(max_length=100)
    date_of_procurement = models.DateField()
    quantity_copies = models.PositiveIntegerField()
    status = models.CharField(max_length=50, default="active")
    serial_no = models.IntegerField(blank=True, null=True)

class UserManagement(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

class Transaction(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField()
    fine_paid = models.BooleanField(default=False)
    remarks = models.TextField(blank=True)
