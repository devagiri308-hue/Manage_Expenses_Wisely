from django.urls import path

from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path(
        'add/',
        views.add_expense,
        name='add_expense'
    ),

    path(
        'expenses/',
        views.expense_list,
        name='expense_list'
    ),
    
    path(
        'edit/<int:pk>/',
        views.edit_expense,
        name='edit_expense'
    ),
    
    path(
        'delete/<int:pk>/',
        views.delete_expense,
        name='delete_expense'
    ),
    
    path(
        'salary-settings/',
        views.salary_settings,
        name='salary_settings'
    ),
    
    path(
        'savings-goals/',
        views.savings_goals,
        name='savings_goals'
    ),
    
    path(
        'savings-goals/add/',
        views.add_savings_goal,
        name='add_savings_goal'
    ),
    
    path(
    'delete-goal/<int:pk>/',
    views.delete_savings_goal,
    name='delete_savings_goal'
    ),
]