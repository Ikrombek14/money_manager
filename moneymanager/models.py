from django.contrib.auth.models import User
from django.db import models

# Create your models here.a
class AccountType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class IncomeCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ExpenseCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name




class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(IncomeCategory, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    date = models.DateField()
    account_type = models.ForeignKey(AccountType, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} - {self.category} - {self.amount}'

class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(ExpenseCategory, on_delete=models.DO_NOTHING)
    amount = models.FloatField()
    date = models.DateField()
    account_type = models.ForeignKey(AccountType, on_delete=models.DO_NOTHING)
    description = models.TextField(blank=True)


    def __str__(self):
        return f'{self.user.username} - {self.category} - {self.amount}'