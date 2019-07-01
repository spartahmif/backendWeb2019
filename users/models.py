from django.db import models
from django.contrib.auth.models import AbstractUser
 
from .managers import CustomUserManager
from .validators import NIMValidator, PhoneValidator
from django.utils.translation import gettext_lazy as _
 
# Create your models here.
 
majors = [
    ('IF','IF'),
    ('STI','STI')
]
 
blood_types = [
    ('A','A'),
    ('B','B'),
    ('AB','AB'),
    ('O','O')
]
 
class CustomUser(AbstractUser):
    nim_validator = NIMValidator()
    phone_validator = PhoneValidator()
 
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=False,
        null=True,
        blank=True
    )
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True, null=True)
    email = models.EmailField(_('email address'), blank=True, null=True)
 
    name = models.CharField(max_length=255)
    nim = models.CharField(
        max_length=20,
        unique=True,
        help_text=_('Required. 20 characters or fewer. Numbers only.'),
        validators=[nim_validator],
        error_messages={
            'unique': _("A user with that NIM already exists."),
        },)
 
    major = models.CharField(max_length=50, choices=majors, blank=True, null=True)
   
    birth_date = models.DateField(max_length=10, blank=True, null=True)
    birth_place = models.CharField(max_length=50, blank=True, null=True)
   
    address = models.TextField(max_length=255, blank=True, null=True)
   
    phone = models.CharField(
        max_length=14,
        validators=[phone_validator],
        blank=True, null=True
        )
   
    blood_type = models.CharField(max_length=50, choices=blood_types, blank=True, null=True)
   
    illness = models.TextField(max_length=255, blank=True, null=True)
 
 
    objects = CustomUserManager()
 
    USERNAME_FIELD = 'nim'
    REQUIRED_FIELDS = ['name']
 
    def __str__(self):
        return self.name