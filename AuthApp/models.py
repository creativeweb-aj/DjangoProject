from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.conf import settings
import calendar
import time


# Custom user manager
class MyUserManager(BaseUserManager):
    def create_user(self, first_name, last_name, date_of_birth, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.first_name = first_name
        user.last_name = last_name
        user.date_of_birth = date_of_birth
        user.created_on = calendar.timegm(time.gmtime())
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


# custom user modal
class MyUserAccount(AbstractBaseUser):
    first_name = models.CharField(verbose_name='First Name', max_length=100, null=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=100, null=True)
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True, )
    password = models.CharField(verbose_name='Password', max_length=100, null=True)
    date_of_birth = models.CharField(verbose_name='Date of Birth', max_length=100, null=True)
    created_on = models.CharField(verbose_name='Join Date', max_length=100, null=True)
    updated_on = models.CharField(verbose_name='Update Date', max_length=100, null=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


# email handler table
class emailHandler(models.Model):
    subject = models.CharField(max_length=255)
    email = models.EmailField()
    body = models.TextField()
    is_sent = models.BooleanField(default=False)
    created_on = models.CharField(max_length=40)
    updated_on = models.CharField(max_length=40)

