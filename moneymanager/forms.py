from django import forms
from .models import Income, Expense
from django.utils import timezone

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['amount', 'date', 'category', 'account_type', 'description']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.initial.get('date'):
            self.fields['date'].initial = timezone.now().date()


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['amount', 'date', 'category', 'account_type', 'description']
        widgets = {
            'date': forms.DateInput(
                attrs={'type': 'date'},
                format='%Y-%m-%d'
            ),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        if not self.initial.get('date'):
            self.fields['date'].initial = timezone.now().date()