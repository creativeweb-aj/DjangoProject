from .models import *
from .serializers import *
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import calendar
import time
import threading
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
        message = render_to_string('acc_active_email.html', {'OTP': token, 'email': email_id})
        email = emailHandler()
        email.user = user
        email.email_id = email_id
        email.subject = mail_subject
        email.body = message
        email.token = token
        email.created_on = calendar.timegm(time.gmtime())
        email.save()
        # start thread
        t = threading.Thread(target=self.getEmailData, args=(), kwargs={})
        print("process started")
        t.setDaemon(True)
        t.start()

    def sendEmail(self, email, subject, body):
        mail = EmailMessage(subject, body, to=[email])
        mail.content_subtype = "html"
        is_sent = mail.send(fail_silently=False)
        if is_sent:
            emailObj = emailHandler.objects.get(email_id=email)
            emailObj.is_sent = True
            emailObj.sent_on = calendar.timegm(time.gmtime())
            emailObj.is_expiry = calendar.timegm(time.gmtime())
            emailObj.updated_on = calendar.timegm(time.gmtime())
            emailObj.retry_count += 1
            emailObj.save()
        else:
            emailObj = emailHandler.objects.get(email_id=email)
            emailObj.is_sent = False
            emailObj.updated_on = calendar.timegm(time.gmtime())
            emailObj.retry_count += 1
            emailObj.save()
        return is_sent

    def getEmailData(self):
        emails = emailHandler.objects.filter(is_sent=False, retry_count__lt=10)
        for email in emails:
            self.sendEmail(email.email_id, email.subject, email.body)
        time.sleep(10)


