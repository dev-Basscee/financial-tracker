from django.db import models
from django.contrib.auth.models import User
from accounts.models import Account

class Category(models.Model):
    """Categories for transactions"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color code
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['name']
        unique_together = ['user', 'name']
        verbose_name_plural = 'Categories'
    
    def __str__(self):
        return self.name

class Transaction(models.Model):
    """Model for financial transactions"""
    TRANSACTION_TYPES = [
        ('income', 'Income'),
        ('expense', 'Expense'),
        ('transfer', 'Transfer'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.TextField()
    date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # For transfers
    to_account = models.ForeignKey(Account, on_delete=models.CASCADE, null=True, blank=True, related_name='incoming_transfers')
    
    class Meta:
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.transaction_type.title()}: {self.amount} - {self.description[:50]}"
    
    def save(self, *args, **kwargs):
        """Update account balances when saving transactions"""
        is_new = self.pk is None
        old_transaction = None
        
        if not is_new:
            old_transaction = Transaction.objects.get(pk=self.pk)
        
        super().save(*args, **kwargs)
        
        # Update account balances
        self._update_account_balances(old_transaction, is_new)
    
    def delete(self, *args, **kwargs):
        """Update account balances when deleting transactions"""
        # Reverse the transaction effects
        if self.transaction_type == 'income':
            self.account.balance -= self.amount
        elif self.transaction_type == 'expense':
            self.account.balance += self.amount
        elif self.transaction_type == 'transfer':
            self.account.balance += self.amount
            if self.to_account:
                self.to_account.balance -= self.amount
                self.to_account.save()
        
        self.account.save()
        super().delete(*args, **kwargs)
    
    def _update_account_balances(self, old_transaction, is_new):
        """Helper method to update account balances"""
        if old_transaction:
            # Reverse old transaction effects
            if old_transaction.transaction_type == 'income':
                old_transaction.account.balance -= old_transaction.amount
            elif old_transaction.transaction_type == 'expense':
                old_transaction.account.balance += old_transaction.amount
            elif old_transaction.transaction_type == 'transfer':
                old_transaction.account.balance += old_transaction.amount
                if old_transaction.to_account:
                    old_transaction.to_account.balance -= old_transaction.amount
                    old_transaction.to_account.save()
            old_transaction.account.save()
        
        # Apply new transaction effects
        if self.transaction_type == 'income':
            self.account.balance += self.amount
        elif self.transaction_type == 'expense':
            self.account.balance -= self.amount
        elif self.transaction_type == 'transfer':
            self.account.balance -= self.amount
            if self.to_account:
                self.to_account.balance += self.amount
                self.to_account.save()
        
        self.account.save()

class Budget(models.Model):
    """Budget model for tracking spending limits"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='budgets')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='budgets')
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    period = models.CharField(max_length=20, choices=[
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ], default='monthly')
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user', 'category', 'start_date', 'end_date']
    
    def __str__(self):
        return f"{self.category.name} - {self.amount} ({self.period})"
    
    @property
    def spent_amount(self):
        """Calculate how much has been spent in this budget period"""
        transactions = Transaction.objects.filter(
            user=self.user,
            category=self.category,
            transaction_type='expense',
            date__date__gte=self.start_date,
            date__date__lte=self.end_date
        )
        return sum(t.amount for t in transactions)
    
    @property
    def remaining_amount(self):
        """Calculate remaining budget amount"""
        return self.amount - self.spent_amount
