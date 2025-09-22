from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Transaction, Budget
from accounts.serializers import AccountSummarySerializer

class CategorySerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Category
        fields = ['id', 'user', 'name', 'description', 'color', 'is_active', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    account = AccountSummarySerializer(read_only=True)
    account_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    to_account = AccountSummarySerializer(read_only=True)
    to_account_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'account', 'account_id', 'category', 'category_id', 
                 'transaction_type', 'amount', 'description', 'date', 'to_account', 
                 'to_account_id', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
    
    def validate(self, data):
        # Validate that transfer transactions have a to_account
        if data.get('transaction_type') == 'transfer' and not data.get('to_account_id'):
            raise serializers.ValidationError("Transfer transactions must specify a destination account.")
        
        # Validate that non-transfer transactions don't have a to_account
        if data.get('transaction_type') != 'transfer' and data.get('to_account_id'):
            raise serializers.ValidationError("Only transfer transactions can have a destination account.")
        
        return data
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        
        # Get account objects
        from accounts.models import Account
        account_id = validated_data.pop('account_id')
        to_account_id = validated_data.pop('to_account_id', None)
        category_id = validated_data.pop('category_id', None)
        
        try:
            account = Account.objects.get(id=account_id, user=validated_data['user'])
            validated_data['account'] = account
        except Account.DoesNotExist:
            raise serializers.ValidationError("Account not found or doesn't belong to user.")
        
        if to_account_id:
            try:
                to_account = Account.objects.get(id=to_account_id, user=validated_data['user'])
                validated_data['to_account'] = to_account
            except Account.DoesNotExist:
                raise serializers.ValidationError("Destination account not found or doesn't belong to user.")
        
        if category_id:
            try:
                category = Category.objects.get(id=category_id, user=validated_data['user'])
                validated_data['category'] = category
            except Category.DoesNotExist:
                raise serializers.ValidationError("Category not found or doesn't belong to user.")
        
        return super().create(validated_data)

class BudgetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    category = CategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    spent_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    remaining_amount = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    
    class Meta:
        model = Budget
        fields = ['id', 'user', 'category', 'category_id', 'amount', 'period', 
                 'start_date', 'end_date', 'is_active', 'spent_amount', 
                 'remaining_amount', 'created_at', 'updated_at']
        read_only_fields = ['id', 'user', 'spent_amount', 'remaining_amount', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        
        category_id = validated_data.pop('category_id')
        try:
            category = Category.objects.get(id=category_id, user=validated_data['user'])
            validated_data['category'] = category
        except Category.DoesNotExist:
            raise serializers.ValidationError("Category not found or doesn't belong to user.")
        
        return super().create(validated_data)

class TransactionSummarySerializer(serializers.Serializer):
    """Serializer for transaction summaries and analytics"""
    total_income = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=15, decimal_places=2)
    net_amount = serializers.DecimalField(max_digits=15, decimal_places=2)
    transaction_count = serializers.IntegerField()
    period_start = serializers.DateField()
    period_end = serializers.DateField()