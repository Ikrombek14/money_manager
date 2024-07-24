from django.urls import path
from .views import dashboard, add_income, add_expense, all_transactions

app_name = "moneymanager"
urlpatterns = [
    path("", dashboard, name ='home'),
    path("add_income/", add_income, name ='add_income'),
    path("add_expense/", add_expense, name ='add_expense'),
   
    path("all_transactions/", all_transactions, name="all-transactions")
   
]