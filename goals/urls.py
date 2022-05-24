from django.urls import path
from . import views

urlpatterns = [
    path('', views.goals, name='goals'),
    path('add_goal', views.add_goal, name='add_goal'),
    path('remove_goal/<int:id>', views.remove_goal, name='remove_goal'),
    path('edit_goal/<int:id>', views.edit_goal, name='edit_goal'),
    path('goal_description/<int:id>', views.goal_description, name='goal_description'),
]