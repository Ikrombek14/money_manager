from django.shortcuts import render, redirect
from .models import AccountType, IncomeCategory, ExpenseCategory, Income, Expense
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from .forms import IncomeForm, ExpenseForm
from django.utils.dateparse import parse_date
from .utils import get_daily_totals, get_monthly_totals, get_weekly_totals, get_custom_range_totals
from django.http import JsonResponse
from datetime import datetime, timedelta


@login_required
def dashboard(request):
    user = request.user
    incomes = Income.objects.filter(user=user)
    expenses = Expense.objects.filter(user=user)


    total_income = sum(income.amount for income in incomes)
    total_expense = sum(expense.amount for expense in expenses)
    net_profit = total_income - total_expense
    expenses_by_category = expenses.values('category', 'date').annotate(total_amount=Sum('amount')).order_by('category', 'date')
    recent_incomes = Income.objects.filter(user=user).order_by('-date')[:3]
    recent_expenses = Expense.objects.filter(user=user).order_by('-date')[:3]
    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_profit': net_profit,
        'expenses_by_category': expenses_by_category,
        'recent_incomes': recent_incomes,
        'recent_expenses': recent_expenses,
    }

    return render(request, 'index.html', context)



@login_required
def add_income(request):
    user = request.user
    if request.method == 'POST':
        form = IncomeForm(request.POST)
        if form.is_valid():
            income = form.save(commit=False)
            income.user = user
            income.save()
            messages.success(request, 'Income added successfully.')
            return redirect(request.GET.get('next', 'moneymanager:home'))
    else:
        form = IncomeForm()
    return render(request, 'add_income.html', {'form': form})


@login_required
def add_expense(request):
    user = request.user
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = user
            expense.save()
            messages.success(request, 'Expense added successfully.')
            return redirect(request.GET.get('next', 'moneymanager:home'))
    else:
        form = ExpenseForm()
    return render(request, 'add_expense.html', {'form': form})
    
def get_date_range_totals(user, model, start_date, end_date):
    return model.objects.filter(user=user, date__range=[start_date, end_date]).aggregate(total=Sum('amount'))['total'] or 0

@login_required
def all_transactions(request):
    user = request.user

    search_description = request.GET.get('description', '')
    search_amount = request.GET.get('amount', '')
    summary_type = request.GET.get('summary_type', 'daily')

    if summary_type == 'daily':
        income_summary = get_daily_totals(user, Income)
        expense_summary = get_daily_totals(user, Expense)
    elif summary_type == 'weekly':
        income_summary = get_weekly_totals(user, Income)
        expense_summary = get_weekly_totals(user, Expense)
    elif summary_type == 'monthly':
        income_summary = get_monthly_totals(user, Income)
        expense_summary = get_monthly_totals(user, Expense)
    else:
        income_summary = 0
        expense_summary = 0

    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    incomes = Income.objects.filter(user=user)
    expenses = Expense.objects.filter(user=user)

    if start_date and end_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        incomes = incomes.filter(date__range=[start_date, end_date])
        expenses = expenses.filter(date__range=[start_date, end_date])

    if search_description:
        incomes = incomes.filter(description__icontains=search_description)
        expenses = expenses.filter(description__icontains=search_description)

    if search_amount:
        incomes = incomes.filter(amount__icontains=search_amount)
        expenses = expenses.filter(amount__icontains=search_amount)

    income_total = incomes.aggregate(total=Sum('amount'))['total'] or 0
    expense_total = expenses.aggregate(total=Sum('amount'))['total'] or 0

    total_income = incomes.aggregate(total=Sum('amount'))['total'] or 0
    total_expense = expenses.aggregate(total=Sum('amount'))['total'] or 0
    net_profit = total_income - total_expense

    recent_incomes = incomes.order_by('-date')
    recent_expenses = expenses.order_by('-date')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'income_summary': income_summary,
            'expense_summary': expense_summary,
            'recent_incomes': list(recent_incomes.values('date', 'category__name', 'description', 'amount')),
            'recent_expenses': list(recent_expenses.values('date', 'category__name', 'description', 'amount')),
        })

    context = {
        'incomes': incomes,
        'expenses': expenses,
        'total_income': total_income,
        'total_expense': total_expense,
        'net_profit': net_profit,
        'recent_incomes': recent_incomes,
        'recent_expenses': recent_expenses,
        'income_summary': income_summary,
        'expense_summary': expense_summary,
        'summary_type': summary_type,
        'income_total': income_total,
        'expense_total': expense_total,
        'start_date': start_date,
        'end_date': end_date,
    }

    return render(request, 'all_transactions.html', context)