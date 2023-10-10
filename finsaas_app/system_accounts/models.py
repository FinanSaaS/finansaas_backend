from django.db import models
from django.contrib.auth.models import User

class SystemAccount(models.Model):
    owner_user = models.ForeignKey(User, related_name="accounts_as_owner", on_delete=models.PROTECT)
    name = models.CharField(max_length=255)
    registration_number = models.CharField(max_length=14)

    is_active = models.BooleanField(default=True, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    street_number = models.CharField(max_length=50)
    complement = models.CharField(max_length=255, blank=True)
    zip_code = models.CharField(max_length=10)

class PhoneNumber(models.Model):
    PHONE_TYPES = (
        ('mobile', 'Mobile'),
        ('landline', 'Landline'),
    )
    number = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=PHONE_TYPES)
    has_whatsapp = models.BooleanField(default=False)

class Email(models.Model):
    email_address = models.EmailField()
