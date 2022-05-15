from django.contrib.auth.models import User, auth
from django.shortcuts import render, redirect
from django.contrib import messages
# Create your views here.


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'The email is already in use!')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.save()
                messages.success(request, 'You have successfully signed up!')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match!')
            return redirect('register')

    return render(request, 'accounts/register.html')


def login(request):
    if request.method == 'POST':
        password = request.POST['password']
        username = request.POST['username']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'credentials are not valid')
            return redirect('login')

    return render(request, 'accounts/login.html')


def logout(request):
    auth.logout(request)
    messages.success(request, 'You are logged out.')
    return redirect('login')


def login_required(request):
    return render(request, 'accounts/login_required.html')