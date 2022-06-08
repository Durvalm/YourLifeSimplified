from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDoList
from .forms import ToDoListForm
from django.core.paginator import Paginator
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required
def todolist(request):
    """Main function that renders all tasks"""
    # Get Objects from ToDoList model and order by deadline date so it displays in todolist.html
    tasks = ToDoList.objects.filter(user=request.user).order_by('end_date')

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
    tasks = ToDoList.objects.filter(user=request.user, is_completed=False).order_by('end_date')

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
    tasks = ToDoList.objects.filter(user=request.user, is_completed=True).order_by('end_date')

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

        # get objects from database
        task = ToDoList.objects.create(user=request.user, description=description, end_date=end_date, title=title,)
        task.save()

        return redirect('todolist')

    return render(request, 'to_do_list/todolist.html')


def remove_task(request, id):
    """This function removes tasks from the To-Do-List"""
    # Get task id from html and delete it
    tasks = ToDoList.objects.get(user=request.user, id=id)
    tasks.delete()

    return redirect('todolist')


def edit_task(request, id):
    """This function redirects the user to another page so he can edit info"""
    tasks = ToDoList.objects.get(user=request.user, id=id)

    # Get data input from user in html form
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        end_date = request.POST['deadline']

        ToDoList.objects.filter(id=id).update(user=request.user, title=title, description=description, end_date=end_date)
        return redirect('todolist')

    context = {
        'tasks': tasks,
    }

    return render(request, 'to_do_list/todolist_edit.html', context)


def change_status(request, id):
    """Changes Task status when user clicks on 'current' or 'completed' """
    # get data
    tasks = ToDoList.objects.get(user=request.user, id=id)

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
    task = ToDoList.objects.get(user=request.user, id=id)

    context = {
        'task': task,
    }
    return render(request, 'to_do_list/task_description.html', context)

