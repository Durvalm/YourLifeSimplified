from django.urls import path
from . import views

urlpatterns = [
    path('', views.todolist, name='todolist'),
    path('add_task', views.add_task, name='add_task'),
    path('remove_task/<int:id>', views.remove_task, name='remove_task'),
    path('edit_task/<int:id>', views.edit_task, name='edit_task'),

]