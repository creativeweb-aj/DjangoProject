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
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )
        user.set_password(password)
        user.is_active = True
        user.is_admin = True
        user.is_staff = True
        user.created_on = calendar.timegm(time.gmtime())
        user.save(using=self._db)
        return user


# custom user modal
class MyUserAccount(AbstractBaseUser):
    first_name = models.CharField(verbose_name='First Name', max_length=100, null=True)
    last_name = models.CharField(verbose_name='Last Name', max_length=100, null=True)
    profile_picture = models.ImageField(upload_to='profile', null=True)
    email = models.EmailField(verbose_name='Email Address', max_length=255, unique=True, )
    password = models.CharField(verbose_name='Password', max_length=100, null=True)
    contact = models.BigIntegerField(verbose_name='contact', null=True)
    profession = models.CharField(verbose_name='profession', max_length=255, null=True)
    biography = models.TextField(verbose_name='bio', null=True)
    date_of_birth = models.BigIntegerField(verbose_name='Date of Birth', null=True)
    created_on = models.BigIntegerField(verbose_name='Join Date', null=True)
    updated_on = models.BigIntegerField(verbose_name='Update Date', null=True)
    is_active = models.BooleanField(default=False, null=True)
    is_staff = models.BooleanField(default=False, null=True)
    is_admin = models.BooleanField(default=False, null=True)
    is_delete = models.BooleanField(default=False, null=True)

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
    user = models.ForeignKey(MyUserAccount, verbose_name='user id', on_delete=models.SET_NULL, null=True)
    subject = models.CharField(verbose_name='Subject', max_length=255)
    email_id = models.EmailField(verbose_name='Email address', null=True)
    body = models.TextField(verbose_name='Body', null=True)
    token = models.BigIntegerField(verbose_name='Token', null=True)
    is_sent = models.BooleanField(verbose_name='Is sent', default=False, null=True)
    is_verify = models.BooleanField(verbose_name='Is verify', default=False, null=True)
    retry_count = models.IntegerField(verbose_name='Retry counter', default=0, null=True)
    is_expiry = models.BigIntegerField(verbose_name='Is expiry', null=True)
    sent_on = models.BigIntegerField(verbose_name='Sent on', null=True)
    created_on = models.BigIntegerField(verbose_name='Created on', null=True)
    updated_on = models.BigIntegerField(verbose_name='Updated on', null=True)

    def __str__(self):
        return self.email_id


class Follow(models.Model):
    follower = models.ForeignKey(MyUserAccount, related_name='following', on_delete=models.SET_NULL, null=True)
    following = models.ForeignKey(MyUserAccount, related_name='followers', on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('follower', 'following')

    def __unicode__(self):
        return u'%s follows %s' % (self.follower, self.following)