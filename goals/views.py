from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
# Create your views here.


def goals(request):
    """Main function that renders all goals"""
    # Get Objects from Goal model and order by deadline date so it displays in goals.html
    if request.user.is_authenticated:
        goals = Goal.objects.filter(user=request.user).order_by('end_date')
    # If user is a guest, enter with session key
    else:
        if not request.session.session_key:
            request.session.create()
        goals = Goal.objects.filter(user=None, session_key=request.session.session_key).order_by('end_date')

    # Create a paginator with 9 goals per page
    paginator = Paginator(goals, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'goals': page_obj,
    }

    return render(request, 'goals/goals.html', context)


def add_goal(request):
    """This function is used to add a goal from the modal to the database"""

    # Get input from html form
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        end_date = request.POST['deadline']

        # Handle error if date is not included
        if not end_date:
            messages.error(request, 'You must include a date')
            return redirect('goals')

        # Handle error if title was previously inputted
        if Goal.objects.filter(title=title).exists():
            messages.error(request, 'You must input a different title')
            return redirect('goals')

        # If user is authenticated, get objects from database
        if request.user.is_authenticated:
            goal = Goal.objects.create(user=request.user, description=description, end_date=end_date, title=title,)
            goal.save()
        # If user is not authenticated, use sessions to handle guest users
        else:
            if not request.session.session_key:
                request.session.create()
            goal = Goal.objects.create(user=None, title=title, description=description, end_date=end_date, session_key=request.session.session_key)
            goal.save()
            messages.success(request, 'Success! Make sure to log in your account so your goals are saved.')
        return redirect('goals')

    return render(request, 'goals/goals.html')


def remove_goal(request, id):
    """This function removes goals from the To-Do-List"""
    # Get user's data if user is authenticated
    if request.user.is_authenticated:
        # Get goal id from html and delete it
        goals = Goal.objects.get(user=request.user, id=id)
        goals.delete()
    # Get guest's data
    else:
        # If session key doesn't exist, create it
        if not request.session.session_key:
            request.session.create()
        # Get goal id from html and delete it
        goals = Goal.objects.get(user=None, id=id, session_key=request.session.session_key)
        goals.delete()

    return redirect('goals')


def edit_goal(request, id):
    """This function redirects the user to another page so he can edit info"""
    # Get user's data if user is authenticated
    if request.user.is_authenticated:
        goals = Goal.objects.get(user=request.user, id=id)
    # Get guest's data
    else:
        goals = Goal.objects.get(user=None, id=id, session_key=request.session.session_key)

    # Get data input from user in html form
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        end_date = request.POST['deadline']

        # Update goal if user is authenticated
        if request.user.is_authenticated:
            Goal.objects.filter(id=id).update(user=request.user, title=title, description=description, end_date=end_date)
        # Update goal if user is a guest (not authenticated)
        else:
            if not request.session.session_key:
                request.session.create()
            Goal.objects.filter(id=id).update(user=None, title=title, description=description, end_date=end_date, session_key=request.session.session_key)

        return redirect('goals')

    context = {
        'goals': goals,
    }

    return render(request, 'goals/edit_goal.html', context)


def goal_description(request, id):
    """Renders all information of the goal on the screen"""
    # Get goal id and send data to goal_description.html
    if request.user.is_authenticated:
        goal = Goal.objects.get(user=request.user, id=id)
    else:
        goal = Goal.objects.get(user=None, id=id, session_key=request.session.session_key)

    context = {
        'goal': goal,
    }
    return render(request, 'goals/goal_description.html', context)

