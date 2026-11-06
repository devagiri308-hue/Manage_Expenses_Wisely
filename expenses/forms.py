from django import forms
from .models import Expense


class ExpenseForm(forms.ModelForm):

    class Meta:
        model = Expense

        fields = [
            'title',
            'category',
            'amount',
            'date',
            'payment_method',
            'description',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter expense name',
            }),

            'category': forms.Select(attrs={
                'class': 'form-control',
            }),

            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'min': '0.01',
                'step': '0.01',
            }),

            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),

            'payment_method': forms.Select(attrs={
                'class': 'form-control',
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Optional description',
            }),
        }

    def clean_amount(self):
        amount = self.cleaned_data['amount']

        if amount <= 0:
            raise forms.ValidationError(
                'Amount must be greater than zero.'
            )

        return amount