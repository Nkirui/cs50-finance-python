from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

@login_required
def index(request):
    return render(request, 'stocks/portfolio.html')

def login_user(request):

    if request.method == "POST":

        # Get POST params from request
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)

        if user is not None and user.is_active:
            login(request, user)
            return render(request, 'stocks/portfolio.html')
        else:
            return render(request, 'error.html', {'message': 'User is not active in the system'})

    else:
        return render(request, 'login/login.html')

def register_user(request):

    if request.method == "POST":

        # Get POST params from request
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm', '')

        # Validate input
        if not username or not password or not confirm:
            return render(request, "error.html", {'message': 'Please enter a non-empty username and password.'})
        elif password != confirm:
            return render(request, "error.html", {'message': 'Passwords do not match. Please try again.'})

        # Create new user
        user = User.objects.create_user(username, password=password)
        login(request, user)

        return render(request, "stocks/quote.html")

    else:
        # Display registration form
        return render(request, 'login/register.html')


def logout_user(request):
    logout(request)
    return redirect('login')
