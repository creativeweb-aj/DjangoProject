from .models import *
from .serializers import *
from .generateToken import *
from .generateToken import *
from django.http import HttpResponse, JsonResponse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import calendar
import time
import random as r


def otpGen():
    otp = ''
    for i in range(6):
        otp += str(r.randint(0, 9))
    print("your otp")
    print(otp)
    return otp


class emailSendService:
    def saveEmail(self, user):
        print('user from email :: ', user)
        token = otpGen()
        mail_subject = 'Activate your account'
        email_id = user.email
        message = 'This is your one time password. ' \
                  'Enter this in confirm box.' \
                  '' + token + ''
        email = emailHandler()
        email.user = user
        email.email_id = email_id
        email.subject = mail_subject
        email.body = message
        email.token = token
        email.created_on = calendar.timegm(time.gmtime())
        saved = email.save()
        to_email = user
        # email = EmailMessage(mail_subject, message, to=[to_email])
        # is_sent = email.send()
        return saved
