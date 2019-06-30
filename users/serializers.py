from rest_framework import serializers, exceptions
from . import models
from django.conf import settings
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _
from allauth.account.adapter import get_adapter

from rest_auth.registration.serializers import RegisterSerializer
# from rest_auth.serializers import LoginSerializer

from .validators import NIMValidator, nim_present


class CustomRegisterSerializer(RegisterSerializer):
    nim_validator = NIMValidator()

    nim = serializers.CharField(required=True, max_length=20, validators=[nim_validator])
    name = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    def validate_password1(self, password):
        return get_adapter().clean_password(password)

    def validate(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_("The two password fields didn't match."))
        if nim_present(data['nim']):
            raise serializers.ValidationError(_("NIM already exists."))
        return data

    def custom_signup(self, request, user):
        pass

    def get_cleaned_data(self):
        return {
            'email': self.validated_data.get('email', ''),
            'password1': self.validated_data.get('password1', ''),
            'name': self.validated_data.get('name', ''),
            'nim': self.validated_data.get('nim', ''),
        }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.name = self.cleaned_data.get('name')
        user.nim = self.cleaned_data.get('nim')
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        user.save()
        return user


class CustomLoginSerializer(serializers.Serializer):
    nim = serializers.CharField(required=True, allow_blank=False)
    password = serializers.CharField(style={'input_type': 'password'})

    def authenticate(self, **kwargs):
        return authenticate(self.context['request'], **kwargs)

    def _validate_username(self, nim, password):
        user = None

        if nim and password:
            user = self.authenticate(nim=nim, password=password)
        else:
            msg = _('Must include "username" and "password".')
            raise exceptions.ValidationError(msg)

        return user

    def validate(self, attrs):
        nim = attrs.get('nim')
        password = attrs.get('password')

        user = None

        if 'allauth' in settings.INSTALLED_APPS:
            from allauth.account import app_settings

            # Authentication through nim
            user = self._validate_username(nim, password)

        else:
            # Authentication without using allauth

            if nim:
                user = self._validate_username(nim, password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise exceptions.ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise exceptions.ValidationError(msg)

        attrs['user'] = user
        return attrs

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomUser
        fields = '__all__'