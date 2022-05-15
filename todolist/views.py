from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .models import ToDoList
from .forms import ToDoListForm
# Create your views here.


def todolist(request):
    # Get Objects from ToDoList model and order by deadline date so it displays in todolist.html

    if request.user.is_authenticated:
        tasks = ToDoList.objects.filter(user=request.user).order_by('end_date')
    else:
        return redirect('login_required')

    context = {
        'tasks': tasks,
    }

    return render(request, 'to_do_list/todolist.html', context)


def add_task(request):
    """This function is used to add a task from the modal to the database"""

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        end_date = request.POST['deadline']

        task = ToDoList.objects.create(user=request.user, title=title, description=description, end_date=end_date)
        task.save()
        return redirect('todolist')

    return render(request, 'to_do_list/todolist.html')


def remove_task(request, id):
    """This function removes tasks from the To-Do-List"""
    tasks = ToDoList.objects.get(user=request.user, id=id)
    tasks.delete()
    return redirect('todolist')


def edit_task(request, id):
    """This function redirects the user to another page so he can edit info"""
    tasks = ToDoList.objects.get(user=request.user, id=id)

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


