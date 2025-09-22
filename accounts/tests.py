from django.test import TestCase
from django.contrib.auth.models import User
from decimal import Decimal
from .models import Account, UserProfile

class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_create_account(self):
        """Test creating a new account"""
        account = Account.objects.create(
            user=self.user,
            name='Test Checking',
            account_type='checking',
            balance=Decimal('1000.00'),
            currency='USD'
        )
        
        self.assertEqual(account.user, self.user)
        self.assertEqual(account.name, 'Test Checking')
        self.assertEqual(account.account_type, 'checking')
        self.assertEqual(account.balance, Decimal('1000.00'))
        self.assertEqual(account.currency, 'USD')
        self.assertTrue(account.is_active)
    
    def test_account_string_representation(self):
        """Test account string representation"""
        account = Account.objects.create(
            user=self.user,
            name='Test Savings',
            account_type='savings',
            balance=Decimal('5000.00'),
            currency='USD'
        )
        
        expected_str = "Test Savings (Savings Account) - USD 5000.00"
        self.assertEqual(str(account), expected_str)
    
    def test_user_profile_creation(self):
        """Test user profile creation"""
        profile = UserProfile.objects.create(
            user=self.user,
            default_currency='EUR',
            timezone='Europe/London',
            monthly_budget=Decimal('2500.00')
        )
        
        self.assertEqual(profile.user, self.user)
        self.assertEqual(profile.default_currency, 'EUR')
        self.assertEqual(profile.timezone, 'Europe/London')
        self.assertEqual(profile.monthly_budget, Decimal('2500.00'))
