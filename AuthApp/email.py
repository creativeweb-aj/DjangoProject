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


class emailSendService:
    def sendEmail(self, user):
        mail_subject = 'Activate your blog account.'
        message = render_to_string('acc_active_email.html', {
            'user': user,
            'domain': get_current_site,
            'uid': urlsafe_base64_encode(force_bytes(user)),
            'token': account_activation_token.make_token(user),
        })
        print('user :: ', user)
        print('domain :: ', get_current_site)
        print('uid :: ', urlsafe_base64_encode(force_bytes(user)))
        print('token generate :: ', account_activation_token.make_token(user))
        to_email = user
        email = EmailMessage(mail_subject, message, to=[to_email])
        is_sent = email.send()
        return is_sent
