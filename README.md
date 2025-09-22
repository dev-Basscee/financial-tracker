# Financial Tracker Backend

A Django REST API backend for a personal financial tracking application. This system helps users track their funds across multiple accounts, categorize transactions, set budgets, and monitor spending patterns.

## Features

- **Account Management**: Support for multiple account types (checking, savings, credit cards, cash, investments)
- **Transaction Tracking**: Record income, expenses, and transfers between accounts
- **Category Management**: Organize transactions with customizable categories
- **Budget Planning**: Set monthly, weekly, or yearly budgets and track spending
- **Real-time Balance Updates**: Automatic balance calculations based on transactions
- **RESTful API**: Full CRUD operations with proper authentication
- **Admin Interface**: Django admin for data management

## Technology Stack

- **Backend**: Django 5.2.6 + Django REST Framework 3.16.1
- **Database**: SQLite (development) / PostgreSQL (production ready)
- **Authentication**: Django Session Authentication
- **API Documentation**: REST Framework browsable API

## Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd financial-tracker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Create sample data (optional):
```bash
python manage.py create_sample_data
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Access the API at `http://localhost:8000/api/`

## API Endpoints

### Base URL: `http://localhost:8000`

### Authentication Endpoints
- `GET /api-auth/login/` - Login page
- `GET /api-auth/logout/` - Logout

### Account Management
- `GET /accounts/api/accounts/` - List user's accounts
- `POST /accounts/api/accounts/` - Create new account
- `GET /accounts/api/accounts/{id}/` - Get account details
- `PUT /accounts/api/accounts/{id}/` - Update account
- `DELETE /accounts/api/accounts/{id}/` - Delete account
- `GET /accounts/api/accounts/summary/` - Get account summary with totals
- `POST /accounts/api/accounts/{id}/toggle_active/` - Toggle account active status

### User Management
- `GET /accounts/api/users/me/` - Get current user info
- `GET /accounts/api/profiles/` - List user profiles
- `POST /accounts/api/profiles/` - Create user profile

### Transaction Management
- `GET /transactions/api/transactions/` - List transactions (with filters)
- `POST /transactions/api/transactions/` - Create new transaction
- `GET /transactions/api/transactions/{id}/` - Get transaction details
- `PUT /transactions/api/transactions/{id}/` - Update transaction
- `DELETE /transactions/api/transactions/{id}/` - Delete transaction
- `GET /transactions/api/transactions/summary/` - Get transaction summary
- `GET /transactions/api/transactions/by_category/` - Group transactions by category

### Category Management
- `GET /transactions/api/categories/` - List categories
- `POST /transactions/api/categories/` - Create new category
- `GET /transactions/api/categories/{id}/` - Get category details
- `PUT /transactions/api/categories/{id}/` - Update category
- `DELETE /transactions/api/categories/{id}/` - Delete category
- `GET /transactions/api/categories/popular/` - Get most used categories

### Budget Management
- `GET /transactions/api/budgets/` - List budgets
- `POST /transactions/api/budgets/` - Create new budget
- `GET /transactions/api/budgets/{id}/` - Get budget details
- `PUT /transactions/api/budgets/{id}/` - Update budget
- `DELETE /transactions/api/budgets/{id}/` - Delete budget
- `GET /transactions/api/budgets/current/` - Get active budgets
- `GET /transactions/api/budgets/alerts/` - Get budget alerts

## Query Parameters

### Transactions
- `type` - Filter by transaction type (income, expense, transfer)
- `account` - Filter by account ID
- `category` - Filter by category ID
- `start_date` - Filter by start date (YYYY-MM-DD)
- `end_date` - Filter by end date (YYYY-MM-DD)

Example: `GET /transactions/api/transactions/?type=expense&start_date=2024-01-01&end_date=2024-01-31`

## Data Models

### Account
- Multiple account types: checking, savings, credit, investment, cash
- Automatic balance tracking
- Multi-currency support
- Active/inactive status

### Transaction
- Three types: income, expense, transfer
- Automatic balance updates
- Category association
- Transfer between accounts

### Category
- User-defined categories
- Color coding
- Usage statistics

### Budget
- Period-based budgeting (weekly, monthly, yearly)
- Spending tracking
- Alert system for overspending

## Authentication

The API uses Django's session-based authentication. To access protected endpoints:

1. Login via `/api-auth/login/`
2. Make authenticated requests with session cookies
3. Logout via `/api-auth/logout/`

For API testing, you can use the browsable API interface provided by Django REST Framework.

## Sample Data

Run the following command to create sample data for testing:

```bash
python manage.py create_sample_data --username testuser
```

This creates:
- Test user with credentials: `testuser` / `testpass123`
- Sample accounts (checking, savings, credit card, cash)
- Sample categories
- Sample transactions
- Sample budgets

## Admin Interface

Access the Django admin at `/admin/` with superuser credentials to manage data directly.

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
The project follows Django conventions and PEP 8 style guidelines.

### Database
- Development: SQLite (default)
- Production: Configure PostgreSQL in settings

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up proper secret key management
4. Configure static file serving
5. Set up HTTPS
6. Configure CORS settings for frontend integration

## License

This project is open source and available under the MIT License.
