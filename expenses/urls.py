from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_expense, name='add_expense'),
    path('list/', views.list_expenses, name='list_expenses'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login')


]