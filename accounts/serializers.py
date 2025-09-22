from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, UserProfile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'default_currency', 'timezone', 'monthly_budget', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

class AccountSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=15, decimal_places=2, read_only=True)
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = Account
        fields = ['id', 'user', 'name', 'account_type', 'balance', 'currency', 
                 'is_active', 'created_at', 'updated_at', 'description']
        read_only_fields = ['id', 'user', 'balance', 'created_at', 'updated_at']
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

class AccountSummarySerializer(serializers.ModelSerializer):
    """Lightweight serializer for account summaries"""
    class Meta:
        model = Account
        fields = ['id', 'name', 'account_type', 'balance', 'currency']