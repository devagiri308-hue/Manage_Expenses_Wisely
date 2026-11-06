from django.shortcuts import render

# Create your views here.
from datetime import date

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404

from .models import Expense, MonthlyIncome ,SavingsGoal
from .forms import ExpenseForm

from datetime import date
from django.db.models import Sum
from dateutil.relativedelta import relativedelta

@login_required
def dashboard(request):

    expenses = Expense.objects.filter(
        user=request.user
    )

    today = date.today()

    today_total = expenses.filter(
        date=today
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0

    monthly_expenses = expenses.filter(
        date__year=today.year,
        date__month=today.month
    )

    monthly_total = monthly_expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0
    # Get the user's monthly salary
    income, created = MonthlyIncome.objects.get_or_create(
        user=request.user,
        defaults={'monthly_salary': 0}
    )

    monthly_salary = income.monthly_salary

    # Calculate estimated savings
    monthly_savings = monthly_salary - monthly_total

# Calculate savings percentage
    if monthly_salary > 0:
        savings_percentage = (
            monthly_savings / monthly_salary
        ) * 100
    else:
        savings_percentage = 0

    overall_total = expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0

    category_totals = (
        monthly_expenses
        .values('category')
        .annotate(total=Sum('amount'))
        .order_by('-total')
    )
    
    highest_category = category_totals.first()

    recent_expenses = expenses.order_by(
        '-date', '-created_at'
    )[:5]
    
    # Monthly spending chart data
    monthly_chart_labels = []
    monthly_chart_values = []

    for i in range(5, -1, -1):
        month_date = today - relativedelta(months=i)

        month_total = expenses.filter(
            date__year=month_date.year,
            date__month=month_date.month
        ).aggregate(
            total=Sum('amount')
        )['total'] or 0

        monthly_chart_labels.append(
            month_date.strftime('%b %Y')
        )

        monthly_chart_values.append(float(month_total))

    # Category-wise spending data
    category_chart_labels = []
    category_chart_values = []

    for item in category_totals:
        category_chart_labels.append(item['category'])
        category_chart_values.append(float(item['total']))

    context = {
        'today_total': today_total,
        'monthly_total': monthly_total,
        'overall_total': overall_total,
        'category_totals': category_totals,
        'recent_expenses': recent_expenses,
        
        'monthly_chart_labels': monthly_chart_labels,
        'monthly_chart_values': monthly_chart_values,
        'category_chart_labels': category_chart_labels,
        'category_chart_values': category_chart_values,
        
        'highest_category': highest_category,
        
        'monthly_salary': monthly_salary,
        'monthly_savings': monthly_savings,
        'savings_percentage': savings_percentage,
    }
    return render(
        request,
        'expenses/dashboard.html',
        context
    )


@login_required
def add_expense(request):

    if request.method == 'POST':
        form = ExpenseForm(request.POST)

        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()

            return redirect('dashboard')

    else:
        form = ExpenseForm()

    return render(
        request,
        'expenses/add_expense.html',
        {'form': form}
    )


@login_required
def expense_list(request):

    expenses = Expense.objects.filter(
        user=request.user
    )

    category = request.GET.get('category')
    search = request.GET.get('search')

    if category:
        expenses = expenses.filter(
            category=category
        )

    if search:
        expenses = expenses.filter(
            title__icontains=search
        )

    return render(
        request,
        'expenses/expense_list.html',
        {
            'expenses': expenses,
            'categories': Expense.CATEGORY_CHOICES,
        }
    )
    
@login_required
def edit_expense(request, pk):

    expense = get_object_or_404(
        Expense,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        form = ExpenseForm(
            request.POST,
            instance=expense
        )

        if form.is_valid():
            form.save()
            return redirect('expense_list')

    else:
        form = ExpenseForm(instance=expense)

    return render(
        request,
        'expenses/edit_expense.html',
        {'form': form, 'expense': expense}
    )


@login_required
def delete_expense(request, pk):

    expense = get_object_or_404(
        Expense,
        pk=pk,
        user=request.user
    )

    if request.method == 'POST':
        expense.delete()
        return redirect('expense_list')

    return render(
        request,
        'expenses/confirm_delete.html',
        {'expense': expense}
    )

@login_required
def salary_settings(request):

    income, created = MonthlyIncome.objects.get_or_create(
        user=request.user,
        defaults={'monthly_salary': 0}
    )

    if request.method == 'POST':
        salary = request.POST.get('monthly_salary')

        if salary:
            try:
                salary = float(salary)

                if salary >= 0:
                    income.monthly_salary = salary
                    income.save()
                    return redirect('dashboard')

            except (ValueError, TypeError):
                pass

    return render(
        request,
        'expenses/salary_settings.html',
        {'income': income}
    )
@login_required
def savings_goals(request):

    goals = SavingsGoal.objects.filter(
        user=request.user
    ).order_by('-created_at')

    return render(
        request,
        'expenses/savings_goals.html',
        {'goals': goals}
    )


@login_required
def add_savings_goal(request):

    if request.method == 'POST':
        goal_name = request.POST.get('goal_name', '').strip()
        target_amount = request.POST.get('target_amount')
        saved_amount = request.POST.get('saved_amount', '0')
        monthly_contribution = request.POST.get('monthly_contribution', '0')

        try:
            target_amount = float(target_amount)
            saved_amount = float(saved_amount or 0)
            monthly_contribution = float(monthly_contribution or 0)

            if (
                goal_name
                and 0 < target_amount
                and 0 <= saved_amount <= target_amount
                and monthly_contribution >= 0
            ):
                SavingsGoal.objects.create(
                    user=request.user,
                    goal_name=goal_name,
                    target_amount=target_amount,
                    saved_amount=saved_amount,
                    monthly_contribution=monthly_contribution
                )

                return redirect('savings_goals')

        except (ValueError, TypeError):
            pass

    return render(
        request,
        'expenses/add_savings_goal.html'
    )
    
from django.views.decorators.http import require_POST

@login_required
@require_POST
def delete_savings_goal(request, pk):

    goal = get_object_or_404(
        SavingsGoal,
        pk=pk,
        user=request.user
    )

    goal.delete()

    return redirect('savings_goals')