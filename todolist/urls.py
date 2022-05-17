from django.urls import path
from . import views

urlpatterns = [
    path('', views.todolist, name='todolist'),
    path('add_task', views.add_task, name='add_task'),
    path('remove_task/<int:id>', views.remove_task, name='remove_task'),
    path('edit_task/<int:id>', views.edit_task, name='edit_task'),
    path('completed_tasks', views.completed_tasks, name='completed_tasks'),
    path('current_tasks', views.current_tasks, name='current_tasks'),
    path('change_status/<int:id>', views.change_status, name='change_status'),
    path('task_description/<int:id>', views.task_description, name='task_description'),
]