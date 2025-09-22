from django.contrib import admin
from .models import Category, Transaction, Budget

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'color', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'user__username']
    readonly_fields = ['created_at']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['description', 'user', 'account', 'transaction_type', 'amount', 'date', 'category']
    list_filter = ['transaction_type', 'date', 'account__account_type', 'category']
    search_fields = ['description', 'user__username', 'account__name']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'date'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'account', 'transaction_type', 'amount', 'description', 'date')
        }),
        ('Categorization', {
            'fields': ('category',)
        }),
        ('Transfer Information', {
            'fields': ('to_account',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ['category', 'user', 'amount', 'period', 'start_date', 'end_date', 'is_active']
    list_filter = ['period', 'is_active', 'start_date']
    search_fields = ['category__name', 'user__username']
    readonly_fields = ['created_at', 'updated_at']
    date_hierarchy = 'start_date'
