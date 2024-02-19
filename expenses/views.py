from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect
from .models import Expense
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django import forms
from .models import Expense
from .models import Category
from django.utils import timezone
from datetime import timedelta
from .forms import ExpenseForm
import random
from django.db.models import Sum


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
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'expenses/login.html', {'form': form})


@login_required
def home(request):
    bank_balance = random.randint(100, 10000)
    now = timezone.now()
    monthly_spend = \
        Expense.objects.filter(user=request.user, date__year=now.year, date__month=now.month).aggregate(Sum('amount'))[
            'amount__sum'] or 0
    top_expense = Expense.objects.filter(user=request.user).order_by('-amount').first()
    return render(request, 'expenses/home.html',
                  {'bank_balance': bank_balance, 'monthly_spend': monthly_spend, 'top_expense': top_expense})


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
    category = request.GET.get('category')
    date = request.GET.get('date')
    expenses = Expense.objects.filter(user=request.user)
    if category == 'others':
        expenses = expenses.exclude(category__name__in=['Food', 'Shopping'])
    elif category:
        expenses = expenses.filter(category__name=category)
    if date == 'latest':
        expenses = expenses.order_by('-date')
    elif date == 'earliest':
        expenses = expenses.order_by('date')
    elif date == 'this_week':
        one_week_ago = timezone.now() - timedelta(days=7)
        expenses = expenses.filter(date__gte=one_week_ago)
    elif date == 'this_month':
        now = timezone.now()
        expenses = expenses.filter(date__year=now.year, date__month=now.month)
    categories = Category.objects.all()
    return render(request, 'expenses/expense_list.html', {'expenses': expenses, 'categories': categories})






def signup(request):
    return render(request, 'expenses/signup.html')
