from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.


def register(request):
    """Sign Up (register) function"""
    # Gets input from html signup form
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # If password and re-enter password are equal
        if password1 == password2:
            # Return error if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, 'The email is already in use!')
                return redirect('register')
            else:
                # if all information is valid, create user
                user = User.objects.create_user(password=password1, username=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, 'You have successfully signed up!')
                return redirect('login')
        # if password and re-enter password are not equal, return error
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

    return render(request, 'accounts/register.html')


def login(request):
    """Login function"""
    # gets input from html login form
    if request.method == 'POST':
        password = request.POST['password']
        email = request.POST['email']

        # authenticates if username and password are matching (using email as username)
        user = auth.authenticate(username=email, password=password)

        # if authenticated, go to home page
        if user is not None:
            auth.login(request, user)
            return redirect('home')
        # if not authenticated, return back to login page
        else:
            messages.error(request, 'credentials are not valid')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    """Logout function"""
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')

def profile(request, id):
    """Allows user to see its own information, and to change password"""
    id = request.user.id

    context = {
        'id': id,
    }

    return render(request, 'accounts/profile.html', context)

def edit_profile(request):
    # get user
    user = request.user

    if request.method == 'POST':
        password = request.POST['password']
        password1 = request.POST['password1']

        if password == password1:
            user.set_password(password)
            user.save()
            messages.success(request, 'Password was successfully changed, please log in again.')
            return redirect('home')


    return render(request, 'accounts/profile.html', context)
