"""
Management command to create sample data for testing the financial tracker
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from accounts.models import Account, UserProfile
from transactions.models import Category, Transaction, Budget
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta

class Command(BaseCommand):
    help = 'Create sample data for testing the financial tracker'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            type=str,
            default='testuser',
            help='Username for the test user'
        )

    def handle(self, *args, **options):
        username = options['username']
        
        # Create or get test user
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                'email': f'{username}@example.com',
                'first_name': 'Test',
                'last_name': 'User'
            }
        )
        
        if created:
            user.set_password('testpass123')
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f'Created test user: {username}')
            )
        
        # Create user profile
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'default_currency': 'USD',
                'timezone': 'UTC',
                'monthly_budget': Decimal('3000.00')
            }
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS('Created user profile')
            )
        
        # Create sample accounts
        accounts_data = [
            {'name': 'Main Checking', 'account_type': 'checking', 'balance': Decimal('2500.00')},
            {'name': 'Savings Account', 'account_type': 'savings', 'balance': Decimal('10000.00')},
            {'name': 'Credit Card', 'account_type': 'credit', 'balance': Decimal('-850.00')},
            {'name': 'Cash Wallet', 'account_type': 'cash', 'balance': Decimal('150.00')},
        ]
        
        created_accounts = []
        for account_data in accounts_data:
            account, created = Account.objects.get_or_create(
                user=user,
                name=account_data['name'],
                defaults={
                    'account_type': account_data['account_type'],
                    'balance': account_data['balance'],
                    'currency': 'USD',
                    'description': f'Sample {account_data["account_type"]} account'
                }
            )
            created_accounts.append(account)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created account: {account.name}')
                )
        
        # Create sample categories
        categories_data = [
            {'name': 'Groceries', 'color': '#FF6B6B', 'description': 'Food and grocery shopping'},
            {'name': 'Transportation', 'color': '#4ECDC4', 'description': 'Gas, public transport, car maintenance'},
            {'name': 'Entertainment', 'color': '#45B7D1', 'description': 'Movies, games, dining out'},
            {'name': 'Utilities', 'color': '#FFA07A', 'description': 'Electricity, water, internet'},
            {'name': 'Salary', 'color': '#98D8C8', 'description': 'Monthly salary income'},
            {'name': 'Healthcare', 'color': '#F7DC6F', 'description': 'Medical expenses, insurance'},
        ]
        
        created_categories = []
        for category_data in categories_data:
            category, created = Category.objects.get_or_create(
                user=user,
                name=category_data['name'],
                defaults={
                    'color': category_data['color'],
                    'description': category_data['description']
                }
            )
            created_categories.append(category)
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created category: {category.name}')
                )
        
        # Create sample transactions
        checking_account = created_accounts[0]  # Main Checking
        savings_account = created_accounts[1]   # Savings Account
        
        # Clear existing balances first
        for account in created_accounts:
            account.balance = Decimal('0.00')
            account.save()
        
        transactions_data = [
            # Income
            {
                'account': checking_account,
                'category': next(c for c in created_categories if c.name == 'Salary'),
                'transaction_type': 'income',
                'amount': Decimal('5000.00'),
                'description': 'Monthly Salary',
                'date': timezone.now() - timedelta(days=25)
            },
            # Expenses
            {
                'account': checking_account,
                'category': next(c for c in created_categories if c.name == 'Groceries'),
                'transaction_type': 'expense',
                'amount': Decimal('120.50'),
                'description': 'Weekly grocery shopping',
                'date': timezone.now() - timedelta(days=20)
            },
            {
                'account': checking_account,
                'category': next(c for c in created_categories if c.name == 'Transportation'),
                'transaction_type': 'expense',
                'amount': Decimal('65.00'),
                'description': 'Gas fill-up',
                'date': timezone.now() - timedelta(days=18)
            },
            {
                'account': checking_account,
                'category': next(c for c in created_categories if c.name == 'Entertainment'),
                'transaction_type': 'expense',
                'amount': Decimal('85.00'),
                'description': 'Dinner at restaurant',
                'date': timezone.now() - timedelta(days=15)
            },
            {
                'account': checking_account,
                'category': next(c for c in created_categories if c.name == 'Utilities'),
                'transaction_type': 'expense',
                'amount': Decimal('150.00'),
                'description': 'Electricity bill',
                'date': timezone.now() - timedelta(days=12)
            },
            # Transfer to savings
            {
                'account': checking_account,
                'transaction_type': 'transfer',
                'amount': Decimal('1000.00'),
                'description': 'Transfer to savings',
                'date': timezone.now() - timedelta(days=10),
                'to_account': savings_account
            },
        ]
        
        for transaction_data in transactions_data:
            transaction, created = Transaction.objects.get_or_create(
                user=user,
                description=transaction_data['description'],
                date=transaction_data['date'],
                defaults=transaction_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created transaction: {transaction.description}')
                )
        
        # Create sample budgets
        budgets_data = [
            {
                'category': next(c for c in created_categories if c.name == 'Groceries'),
                'amount': Decimal('400.00'),
                'period': 'monthly',
                'start_date': timezone.now().date().replace(day=1),
                'end_date': (timezone.now().date().replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            },
            {
                'category': next(c for c in created_categories if c.name == 'Entertainment'),
                'amount': Decimal('200.00'),
                'period': 'monthly',
                'start_date': timezone.now().date().replace(day=1),
                'end_date': (timezone.now().date().replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
            },
        ]
        
        for budget_data in budgets_data:
            budget, created = Budget.objects.get_or_create(
                user=user,
                category=budget_data['category'],
                start_date=budget_data['start_date'],
                end_date=budget_data['end_date'],
                defaults=budget_data
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created budget for {budget.category.name}: ${budget.amount}')
                )
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Sample data creation completed for user: {username}'
            )
        )
        self.stdout.write(
            f'Login credentials: {username} / testpass123'
        )