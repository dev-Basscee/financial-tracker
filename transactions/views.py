from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Sum, Q, Count
from django.utils import timezone
from datetime import datetime, timedelta
from .models import Category, Transaction, Budget
from .serializers import (
    CategorySerializer, TransactionSerializer, BudgetSerializer, 
    TransactionSummarySerializer
)

class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet for managing transaction categories"""
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def popular(self, request):
        """Get most used categories"""
        categories = self.get_queryset().annotate(
            transaction_count=Count('transactions')
        ).order_by('-transaction_count')[:10]
        
        return Response(CategorySerializer(categories, many=True).data)

class TransactionViewSet(viewsets.ModelViewSet):
    """ViewSet for managing financial transactions"""
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Transaction.objects.filter(user=self.request.user)
        
        # Filter by transaction type
        transaction_type = self.request.query_params.get('type', None)
        if transaction_type:
            queryset = queryset.filter(transaction_type=transaction_type)
        
        # Filter by account
        account_id = self.request.query_params.get('account', None)
        if account_id:
            queryset = queryset.filter(account_id=account_id)
        
        # Filter by category
        category_id = self.request.query_params.get('category', None)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        # Filter by date range
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)
        if start_date:
            queryset = queryset.filter(date__date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__date__lte=end_date)
        
        return queryset.order_by('-date')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get transaction summary for a period"""
        # Default to current month if no dates provided
        end_date = timezone.now().date()
        start_date = end_date.replace(day=1)
        
        # Override with query parameters if provided
        if request.query_params.get('start_date'):
            start_date = datetime.strptime(request.query_params.get('start_date'), '%Y-%m-%d').date()
        if request.query_params.get('end_date'):
            end_date = datetime.strptime(request.query_params.get('end_date'), '%Y-%m-%d').date()
        
        transactions = self.get_queryset().filter(
            date__date__gte=start_date,
            date__date__lte=end_date
        )
        
        income_total = transactions.filter(transaction_type='income').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        expense_total = transactions.filter(transaction_type='expense').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        summary_data = {
            'total_income': income_total,
            'total_expenses': expense_total,
            'net_amount': income_total - expense_total,
            'transaction_count': transactions.count(),
            'period_start': start_date,
            'period_end': end_date
        }
        
        serializer = TransactionSummarySerializer(summary_data)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Get transactions grouped by category"""
        # Default to current month
        end_date = timezone.now().date()
        start_date = end_date.replace(day=1)
        
        if request.query_params.get('start_date'):
            start_date = datetime.strptime(request.query_params.get('start_date'), '%Y-%m-%d').date()
        if request.query_params.get('end_date'):
            end_date = datetime.strptime(request.query_params.get('end_date'), '%Y-%m-%d').date()
        
        transactions = self.get_queryset().filter(
            date__date__gte=start_date,
            date__date__lte=end_date
        ).exclude(category__isnull=True)
        
        category_data = {}
        for transaction in transactions:
            category_name = transaction.category.name
            if category_name not in category_data:
                category_data[category_name] = {
                    'category': CategorySerializer(transaction.category).data,
                    'total_amount': 0,
                    'transaction_count': 0,
                    'transactions': []
                }
            
            category_data[category_name]['total_amount'] += float(transaction.amount)
            category_data[category_name]['transaction_count'] += 1
            category_data[category_name]['transactions'].append(
                TransactionSerializer(transaction).data
            )
        
        return Response(list(category_data.values()))

class BudgetViewSet(viewsets.ModelViewSet):
    """ViewSet for managing budgets"""
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Get current active budgets"""
        current_date = timezone.now().date()
        budgets = self.get_queryset().filter(
            is_active=True,
            start_date__lte=current_date,
            end_date__gte=current_date
        )
        
        return Response(BudgetSerializer(budgets, many=True).data)
    
    @action(detail=False, methods=['get'])
    def alerts(self, request):
        """Get budget alerts for overspending"""
        current_date = timezone.now().date()
        budgets = self.get_queryset().filter(
            is_active=True,
            start_date__lte=current_date,
            end_date__gte=current_date
        )
        
        alerts = []
        for budget in budgets:
            spent_percentage = (budget.spent_amount / float(budget.amount)) * 100 if budget.amount > 0 else 0
            
            if spent_percentage >= 100:
                alert_type = 'over_budget'
                message = f"Budget exceeded for {budget.category.name}"
            elif spent_percentage >= 80:
                alert_type = 'warning'
                message = f"80% of budget used for {budget.category.name}"
            else:
                continue
            
            alerts.append({
                'budget': BudgetSerializer(budget).data,
                'alert_type': alert_type,
                'message': message,
                'spent_percentage': round(spent_percentage, 2)
            })
        
        return Response(alerts)
