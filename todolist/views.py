from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDoList
from .forms import ToDoListForm
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
# Create your views here.


def todolist(request):
    """Main function that renders all tasks"""
    # Get Objects from ToDoList model and order by deadline date so it displays in todolist.html
    if request.user.is_authenticated:
        tasks = ToDoList.objects.filter(user=request.user).order_by('end_date')
    # If user is a guest, enter with session key
    else:
        if not request.session.session_key:
            request.session.create()
        tasks = ToDoList.objects.filter(user=None, session_key=request.session.session_key).order_by('end_date')

    # Create a paginator with 9 tasks per page
    paginator = Paginator(tasks, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Change Task Status to 'Missing' if deadline time has passed
    for task in tasks:
        if not task.is_completed:
            if task.end_date < timezone.now():
                task.is_late = True
                task.save()

    context = {
        'tasks': page_obj,
    }

    return render(request, 'to_do_list/todolist.html', context)


def current_tasks(request):
    """This function filters tasks showing only the completed ones"""
    # Get Objects from ToDoList model and order by deadline date so it displays in todolist/current_tasks
    if request.user.is_authenticated:
        tasks = ToDoList.objects.filter(user=request.user, is_completed=False).order_by('end_date')
    # If user is a guest, enter with session key
    else:
        tasks = ToDoList.objects.filter(user=None, session_key=request.session.session_key, is_completed=False) .order_by('end_date')
    # Create a paginator with 9 tasks per page
    paginator = Paginator(tasks, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tasks': page_obj,
    }
    return render(request, 'to_do_list/todolist.html', context)


def completed_tasks(request):
    """This function filters tasks showing only the completed ones"""
    # Get Objects from ToDoList model and order by deadline date so it displays in todolist/current_tasks
    if request.user.is_authenticated:
        tasks = ToDoList.objects.filter(user=request.user, is_completed=True).order_by('end_date')
    # If user is a guest, enter with session key
    else:
        tasks = ToDoList.objects.filter(user=None, session_key=request.session.session_key, is_completed=True).order_by('end_date')
    # Create a paginator with 9 tasks per page
    paginator = Paginator(tasks, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'tasks': page_obj,
    }

    return render(request, 'to_do_list/todolist.html', context)


def add_task(request):
    """This function is used to add a task from the modal to the database"""

    # Get input from html form
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        end_date = request.POST['deadline']

        # Handle error if date is not included
        if not end_date:
            messages.error(request, 'You must include a date')
            return redirect('todolist')

        # Handle error if title was previously inputted
        if ToDoList.objects.filter(title=title).exists():
            messages.error(request, 'You must input a different title')
            return redirect('todolist')

        # If user is authenticated, get objects from database
        if request.user.is_authenticated:
            task = ToDoList.objects.create(user=request.user, description=description, end_date=end_date, title=title,)
            task.save()
        # If user is not authenticated, use sessions to handle guest users
        else:
            if not request.session.session_key:
                request.session.create()
            task = ToDoList.objects.create(user=None, title=title, description=description, end_date=end_date, session_key=request.session.session_key)
            task.save()
            messages.success(request, 'Success! Make sure to log in your account so your tasks are saved.')
        return redirect('todolist')

    return render(request, 'to_do_list/todolist.html')


def remove_task(request, id):
    """This function removes tasks from the To-Do-List"""
    # Get user's data if user is authenticated
    if request.user.is_authenticated:
        # Get task id from html and delete it
        tasks = ToDoList.objects.get(user=request.user, id=id)
        tasks.delete()
    # Get guest's data
    else:
        # If session key doesn't exist, create it
        if not request.session.session_key:
            request.session.create()
        # Get task id from html and delete it
        tasks = ToDoList.objects.get(user=None, id=id, session_key=request.session.session_key)
        tasks.delete()

    return redirect('todolist')


def edit_task(request, id):
    """This function redirects the user to another page so he can edit info"""
    # Get user's data if user is authenticated
    if request.user.is_authenticated:
        tasks = ToDoList.objects.get(user=request.user, id=id)
    # Get guest's data
    else:
        tasks = ToDoList.objects.get(user=None, id=id, session_key=request.session.session_key)

    # Get data input from user in html form
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        end_date = request.POST['deadline']

        # Update task if user is authenticated
        if request.user.is_authenticated:
            ToDoList.objects.filter(id=id).update(user=request.user, title=title, description=description, end_date=end_date)
        # Update task if user is a guest (not authenticated)
        else:
            if not request.session.session_key:
                request.session.create()
            ToDoList.objects.filter(id=id).update(user=None, title=title, description=description, end_date=end_date, session_key=request.session.session_key)

        return redirect('todolist')

    context = {
        'tasks': tasks,
    }

    return render(request, 'to_do_list/todolist_edit.html', context)


def change_status(request, id):
    """Changes Task status when user clicks on 'current' or 'completed' """
    # If user is authenticated, get data
    if request.user.is_authenticated:
        # Get task id from html href
        tasks = ToDoList.objects.get(user=request.user, id=id)
    # if user is guest
    else:
        # Get task id from html href
        tasks = ToDoList.objects.get(user=None, id=id, session_key=request.session.session_key)

    # If task is completed and change_status button is clicked, change it to Current
    if tasks.is_completed:
        tasks.is_completed = False
        tasks.is_late = False
        tasks.save()
        return redirect('todolist')
    # If task is current and change_status button is clicked, change it to completed
    else:
        tasks.is_completed = True
        tasks.is_late = False
        tasks.save()
        return redirect('todolist')


def task_description(request, id):
    """Renders all information of the task on the screen"""
    # Get task id and send data to task_description.html
    if request.user.is_authenticated:
        task = ToDoList.objects.get(user=request.user, id=id)
    else:
        task = ToDoList.objects.get(user=None, id=id, session_key=request.session.session_key)

    context = {
        'task': task,
    }
    return render(request, 'to_do_list/task_description.html', context)

