from django.contrib import admin
from .models import AccountType, IncomeCategory, ExpenseCategory, Income, Expense
# Register your models here.
admin.site.register(AccountType)
admin.site.register(IncomeCategory)
admin.site.register(ExpenseCategory)
admin.site.register(Income)
admin.site.register(Expense)