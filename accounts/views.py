from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.db.models import Sum, Q
from .models import Account, UserProfile
from .serializers import AccountSerializer, UserProfileSerializer, UserSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for user information"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Get current user information"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class UserProfileViewSet(viewsets.ModelViewSet):
    """ViewSet for user profiles"""
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserProfile.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AccountViewSet(viewsets.ModelViewSet):
    """ViewSet for managing financial accounts"""
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        """Get account summary with total balances"""
        accounts = self.get_queryset().filter(is_active=True)
        
        total_balance = accounts.aggregate(
            total=Sum('balance')
        )['total'] or 0
        
        account_types_summary = {}
        for account in accounts:
            account_type = account.account_type
            if account_type not in account_types_summary:
                account_types_summary[account_type] = {
                    'count': 0,
                    'total_balance': 0
                }
            account_types_summary[account_type]['count'] += 1
            account_types_summary[account_type]['total_balance'] += float(account.balance)
        
        return Response({
            'total_balance': total_balance,
            'total_accounts': accounts.count(),
            'account_types': account_types_summary,
            'accounts': AccountSerializer(accounts, many=True).data
        })
    
    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """Toggle account active status"""
        account = self.get_object()
        account.is_active = not account.is_active
        account.save()
        return Response({
            'message': f'Account {"activated" if account.is_active else "deactivated"} successfully',
            'is_active': account.is_active
        })
