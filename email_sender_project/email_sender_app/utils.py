import pandas as pd
from django.core.mail import send_mail
from django.conf import settings

from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags

def parse_excel(file):
    df = pd.read_excel(file)  # You can also support CSV with pd.read_csv
    email_list = df.iloc[:, 0].dropna().tolist()  # Assumes emails are in the first column
    return email_list


# Sending HTML code 
def send_bulk_email(subject, html_message, email_list):
    plain_message = strip_tags(html_message)  # fallback for non-HTML clients

    for email in email_list:
        msg = EmailMultiAlternatives(
            subject=subject,
            body=plain_message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email],
        )
        msg.attach_alternative(html_message, "text/html")
        msg.send()


# Sending text only

# def send_bulk_email(subject, message, recipient_list):
#     for email in recipient_list:
#         send_mail(
#             subject,
#             message,
#             settings.EMAIL_HOST_USER,
#             [email],
#             fail_silently=False,
#         )
