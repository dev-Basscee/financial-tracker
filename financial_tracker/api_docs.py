from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

@api_view(['GET'])
@permission_classes([AllowAny])
def api_documentation(request):
    """
    API Documentation endpoint providing information about all available endpoints
    """
    docs = {
        "title": "Financial Tracker API Documentation",
        "version": "1.0.0",
        "description": "REST API for personal financial tracking and management",
        "base_url": request.build_absolute_uri('/'),
        "authentication": {
            "type": "Session Authentication",
            "login_url": "/api-auth/login/",
            "logout_url": "/api-auth/logout/"
        },
        "endpoints": {
            "accounts": {
                "base_url": "/accounts/api/",
                "endpoints": {
                    "accounts": {
                        "list": "GET /accounts/api/accounts/",
                        "create": "POST /accounts/api/accounts/",
                        "detail": "GET /accounts/api/accounts/{id}/",
                        "update": "PUT /accounts/api/accounts/{id}/",
                        "delete": "DELETE /accounts/api/accounts/{id}/",
                        "summary": "GET /accounts/api/accounts/summary/",
                        "toggle_active": "POST /accounts/api/accounts/{id}/toggle_active/"
                    },
                    "users": {
                        "me": "GET /accounts/api/users/me/"
                    },
                    "profiles": {
                        "list": "GET /accounts/api/profiles/",
                        "create": "POST /accounts/api/profiles/"
                    }
                }
            },
            "transactions": {
                "base_url": "/transactions/api/",
                "endpoints": {
                    "transactions": {
                        "list": "GET /transactions/api/transactions/",
                        "create": "POST /transactions/api/transactions/",
                        "detail": "GET /transactions/api/transactions/{id}/",
                        "update": "PUT /transactions/api/transactions/{id}/",
                        "delete": "DELETE /transactions/api/transactions/{id}/",
                        "summary": "GET /transactions/api/transactions/summary/",
                        "by_category": "GET /transactions/api/transactions/by_category/"
                    },
                    "categories": {
                        "list": "GET /transactions/api/categories/",
                        "create": "POST /transactions/api/categories/",
                        "detail": "GET /transactions/api/categories/{id}/",
                        "update": "PUT /transactions/api/categories/{id}/",
                        "delete": "DELETE /transactions/api/categories/{id}/",
                        "popular": "GET /transactions/api/categories/popular/"
                    },
                    "budgets": {
                        "list": "GET /transactions/api/budgets/",
                        "create": "POST /transactions/api/budgets/",
                        "detail": "GET /transactions/api/budgets/{id}/",
                        "update": "PUT /transactions/api/budgets/{id}/",
                        "delete": "DELETE /transactions/api/budgets/{id}/",
                        "current": "GET /transactions/api/budgets/current/",
                        "alerts": "GET /transactions/api/budgets/alerts/"
                    }
                }
            }
        },
        "query_parameters": {
            "transactions": {
                "type": "Filter by transaction type (income, expense, transfer)",
                "account": "Filter by account ID",
                "category": "Filter by category ID", 
                "start_date": "Filter by start date (YYYY-MM-DD)",
                "end_date": "Filter by end date (YYYY-MM-DD)"
            }
        },
        "sample_requests": {
            "create_account": {
                "url": "POST /accounts/api/accounts/",
                "data": {
                    "name": "My Checking Account",
                    "account_type": "checking",
                    "currency": "USD",
                    "description": "Primary checking account"
                }
            },
            "create_transaction": {
                "url": "POST /transactions/api/transactions/",
                "data": {
                    "account_id": 1,
                    "category_id": 1,
                    "transaction_type": "expense",
                    "amount": "50.00",
                    "description": "Grocery shopping",
                    "date": "2024-01-15T10:30:00Z"
                }
            },
            "create_budget": {
                "url": "POST /transactions/api/budgets/",
                "data": {
                    "category_id": 1,
                    "amount": "400.00",
                    "period": "monthly",
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-31"
                }
            }
        }
    }
    
    return Response(docs)