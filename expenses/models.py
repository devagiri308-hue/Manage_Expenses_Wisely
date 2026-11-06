from django.db import models
from django.contrib.auth.models import User


class Expense(models.Model):

    CATEGORY_CHOICES = [
        ('groceries', 'Supermarket & Groceries'),
        ('fuel', 'Petrol & Fuel'),
        ('food', 'Food & Restaurants'),
        ('shopping', 'Shopping & Clothes'),
        ('electricity', 'Electricity Bill'),
        ('water', 'Water Bill'),
        ('internet', 'Internet & Mobile Recharge'),
        ('rent', 'House Rent'),
        ('transport', 'Transportation'),
        ('medical', 'Medical Expenses'),
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('travel', 'Travel'),
        ('emi', 'EMI & Loan Payments'),
        ('family', 'Family Expenses'),
        ('other', 'Other Expenses'),
    ]

    PAYMENT_CHOICES = [
        ('cash', 'Cash'),
        ('upi', 'UPI'),
        ('card', 'Debit/Credit Card'),
        ('bank', 'Bank Transfer'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='expenses'
    )

    title = models.CharField(max_length=200)

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    date = models.DateField()

    payment_method = models.CharField(
        max_length=10,
        choices=PAYMENT_CHOICES,
        default='cash'
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"
    
# Create your models here.

class MonthlyIncome(models.Model):
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='monthly_income'
    )

    monthly_salary = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.user.username} - ₹{self.monthly_salary}"
class SavingsGoal(models.Model):
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='savings_goals'
    )

    goal_name = models.CharField(max_length=100)

    target_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    saved_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    monthly_contribution = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.goal_name} - ₹{self.target_amount}"

    @property
    def remaining_amount(self):
        remaining = self.target_amount - self.saved_amount
        return max(remaining, 0)

    @property
    def progress_percentage(self):
        if self.target_amount > 0:
            percentage = (
                self.saved_amount / self.target_amount
            ) * 100
            return min(percentage, 100)

        return 0

    @property
    def months_remaining(self):
        if self.monthly_contribution > 0:
            remaining = self.remaining_amount
            return int(
                (remaining + self.monthly_contribution - 1)
                // self.monthly_contribution
            ) if remaining > 0 else 0

        return None