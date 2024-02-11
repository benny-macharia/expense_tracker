from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'description', 'category']


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'expenses/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('list_expenses')
    else:
        form = AuthenticationForm()

    return render(request, 'expenses/login.html', {'form': form})


from .forms import ExpenseForm  # make sure you have this form defined


def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            new_expense = form.save(commit=False)
            new_expense.user = request.user
            new_expense.save()
            return redirect('list_expenses')
    else:
        form = ExpenseForm()

    return render(request, 'expenses/expense_form.html', {'form': form})


def list_expenses(request):
    expenses = Expense.objects.filter(user=request.user)
    return render(request, 'expenses/expense_list.html', {'expenses': expenses})
