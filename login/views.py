from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from stocks.models import FinanceUser

@login_required
def index(request):
    return redirect('portfolio')

def login_user(request):

    if request.method == "POST":

        # Get POST params from request
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)

        # Valid username and password
        if user is not None and user.is_active:
            login(request, user)
            return redirect('portfolio')
        # Incorrect username or password
        elif user is None:
            return render(request, "error.html", {'message': 'Invalid username and/or password'})
        # User is inactive
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

        # Make sure a user with this username doesn't already exist
        try:
            User.objects.get(username=username)
            return render(request, "error.html", {
                'message': 'A user with that username already exists in the system. Please choose another username'
            })
        except User.DoesNotExist:
            pass

        # Validate input
        if not username or not password or not confirm:
            return render(request, "error.html", {'message': 'Please enter a non-empty username and password.'})
        elif password != confirm:
            return render(request, "error.html", {'message': 'Passwords do not match. Please try again.'})

        # Create new user
        user = User.objects.create_user(username, password=password)
        FinanceUser.objects.create(user=user, cash=10000)

        # Login new user
        user = authenticate(username=username, password=password)
        login(request, user)

        # Send the newly logged in user to the quote page
        return redirect('quote')

    else:
        # Display registration form
        return render(request, 'login/register.html')


def logout_user(request):
    logout(request)
    return redirect('login')
