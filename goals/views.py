from django.shortcuts import render

# Create your views here.

from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import Goal
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def goals(request):
    """Main function that renders all goals"""
    # Get Objects from Goal model and order by deadline date so it displays in goals.html
    goals = Goal.objects.filter(user=request.user).order_by('end_date')

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

        # get objects from database
        goal = Goal.objects.create(user=request.user, description=description, end_date=end_date, title=title,)
        goal.save()

        return redirect('goals')

    return render(request, 'goals/goals.html')


def remove_goal(request, id):
    """This function removes goals from the To-Do-List"""
    # Get goal id from html and delete it
    goals = Goal.objects.get(user=request.user, id=id)
    goals.delete()

    return redirect('goals')


def edit_goal(request, id):
    """This function redirects the user to another page so he can edit info"""
    # Get user's data
    goals = Goal.objects.get(user=request.user, id=id)

    # Get data input from user in html form
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        end_date = request.POST['deadline']

        # Update goal if user is authenticated
        Goal.objects.filter(id=id).update(user=request.user, title=title, description=description, end_date=end_date)
        return redirect('goals')

    context = {
        'goals': goals,
    }

    return render(request, 'goals/edit_goal.html', context)


def goal_description(request, id):
    """Renders all information of the goal on the screen"""
    # Get goal id and send data to goal_description.html
    goal = Goal.objects.get(user=request.user, id=id)

    context = {
        'goal': goal,
    }
    return render(request, 'goals/goal_description.html', context)

