from home.models import Student
import time
from django.core.mail import send_mail, EmailMessage
from django.conf import settings

def run_this_function():
    print("Function Started")
    time.sleep(1)
    print("Function Started")
    

def send_email_to_client():
    subject = "This email if from Django Server"
    message = "This is a Demo Message from Django "
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["ash75356@gmail.com"]
    send_mail(subject, message, from_email, recipient_list)