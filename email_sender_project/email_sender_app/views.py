from django.shortcuts import redirect, render
from .forms import EmailForm, LoginForm
from .utils import parse_excel, send_bulk_email
from django.contrib import messages

def index(request):

    if 'username' not in request.session:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')  # Redirect to the login page if not logged in
    
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

# Fixed login credentials
FIXED_USERNAME = "admin"
FIXED_PASSWORD = "Tech@123"

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check if the entered credentials match the fixed ones
            if username == FIXED_USERNAME and password == FIXED_PASSWORD:
                # Create a user session (login)
                request.session['username'] = username
                messages.success(request, "Login successful!")
                return redirect('index')  # Redirect to a home page or any page
            else:
                messages.error(request, "Invalid credentials.")
    else:
        form = LoginForm()

    return render(request, 'email_sender_app/login.html', {'form': form})

def logout_view(request):
    # Clear the user session to log them out
    if 'username' in request.session:
        del request.session['username']
        messages.success(request, "You have been logged out successfully.")
    return redirect('login')  # Redirect to the login page after logout