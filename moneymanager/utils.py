from django.db.models import Sum
from datetime import datetime, timedelta

def get_daily_totals(user, model):
    today = datetime.today().date()
    result = model.objects.filter(user=user, date=today).aggregate(Sum('amount'))
    daily_total = result.get('amount__sum', 0) or 0
    return daily_total

def get_weekly_totals(user, model):
    today = datetime.today().date()
    start_of_week = today - timedelta(days=today.weekday())
    result = model.objects.filter(user=user, date__range=[start_of_week, today]).aggregate(Sum('amount'))
    weekly_total = result.get('amount__sum', 0) or 0
    return weekly_total

def get_monthly_totals(user, model):
    today = datetime.today().date()
    start_of_month = today.replace(day=1)
    result = model.objects.filter(user=user, date__range=[start_of_month, today]).aggregate(Sum('amount'))
    monthly_total = result.get('amount__sum', 0) or 0
    return monthly_total

def get_custom_range_totals(user, model, start_date, end_date):
    result = model.objects.filter(user=user, date__range=[start_date, end_date]).aggregate(Sum('amount'))
    custom_total = result.get('amount__sum', 0) or 0
    return custom_total
