import re
 
from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
 
 
def nim_present(nim):
    User = get_user_model()
    if User.objects.filter(nim=nim).exists():
        return True  
    return False
 
@deconstructible
class NIMValidator(validators.RegexValidator):
    regex = r'^[\d]+$'
    message = _(
        'Enter a valid NIM. This value may contain only numbers'
    )
    flags = 0
 
@deconstructible
class PhoneValidator(validators.RegexValidator):
    regex = '^\d{9,14}$'
    message = _(
        'Enter a valid phone number, between 9 - 14 digits'
    )
    flags = 0