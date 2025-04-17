from django.shortcuts import render
from .forms import EmailForm
from .utils import parse_excel, send_bulk_email
from django.contrib import messages

def index(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            file = form.cleaned_data['file']

            try:
                email_list = parse_excel(file)
                send_bulk_email(subject, message, email_list)
                messages.success(request, 'Emails sent successfully!')
            except Exception as e:
                messages.error(request, f'Error sending emails: {e}')
    else:
        form = EmailForm()
    return render(request, 'email_sender_app/index.html', {'form': form})
