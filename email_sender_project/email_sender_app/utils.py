import pandas as pd
from django.core.mail import send_mail
from django.conf import settings

def parse_excel(file):
    df = pd.read_excel(file)  # You can also support CSV with pd.read_csv
    email_list = df.iloc[:, 0].dropna().tolist()  # Assumes emails are in the first column
    return email_list

def send_bulk_email(subject, message, recipient_list):
    for email in recipient_list:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
