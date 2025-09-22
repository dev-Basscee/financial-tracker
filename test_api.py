#!/usr/bin/env python3
"""
Simple test script to demonstrate the Financial Tracker API functionality
"""

import requests
import json
from datetime import datetime, timedelta

# Configuration
BASE_URL = "http://localhost:8000"
USERNAME = "testuser"
PASSWORD = "testpass123"

class FinancialTrackerAPITest:
    def __init__(self):
        self.session = requests.Session()
        self.base_url = BASE_URL
        
    def login(self):
        """Login to get session authentication"""
        # Get login page to get CSRF token
        login_page = self.session.get(f"{self.base_url}/api-auth/login/")
        
        if 'csrftoken' in self.session.cookies:
            csrf_token = self.session.cookies['csrftoken']
        else:
            # Try to extract from page content
            csrf_token = None
            
        # Login with credentials
        login_data = {
            'username': USERNAME,
            'password': PASSWORD,
        }
        
        if csrf_token:
            login_data['csrfmiddlewaretoken'] = csrf_token
            
        response = self.session.post(
            f"{self.base_url}/api-auth/login/",
            data=login_data,
            headers={'Referer': f"{self.base_url}/api-auth/login/"}
        )
        
        return response.status_code in [200, 302]
    
    def test_api_endpoints(self):
        """Test various API endpoints"""
        print("=== Financial Tracker API Test ===\n")
        
        # Test API root
        response = self.session.get(f"{self.base_url}/api/")
        print("1. API Root:")
        print(json.dumps(response.json(), indent=2))
        print()
        
        # Test accounts summary
        response = self.session.get(f"{self.base_url}/accounts/api/accounts/summary/")
        if response.status_code == 200:
            print("2. Accounts Summary:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"2. Accounts Summary - Error: {response.status_code}")
        print()
        
        # Test transactions summary
        response = self.session.get(f"{self.base_url}/transactions/api/transactions/summary/")
        if response.status_code == 200:
            print("3. Transactions Summary:")
            print(json.dumps(response.json(), indent=2))
        else:
            print(f"3. Transactions Summary - Error: {response.status_code}")
        print()
        
        # Test categories
        response = self.session.get(f"{self.base_url}/transactions/api/categories/")
        if response.status_code == 200:
            categories = response.json()
            print(f"4. Categories ({len(categories['results']) if 'results' in categories else len(categories)} total):")
            for category in (categories['results'] if 'results' in categories else categories):
                print(f"   - {category['name']} ({category['color']})")
        else:
            print(f"4. Categories - Error: {response.status_code}")
        print()
        
        # Test budgets
        response = self.session.get(f"{self.base_url}/transactions/api/budgets/current/")
        if response.status_code == 200:
            budgets = response.json()
            print(f"5. Current Budgets ({len(budgets)} total):")
            for budget in budgets:
                print(f"   - {budget['category']['name']}: ${budget['amount']} "
                      f"(Spent: ${budget['spent_amount']}, Remaining: ${budget['remaining_amount']})")
        else:
            print(f"5. Current Budgets - Error: {response.status_code}")
        print()
        
        # Test budget alerts
        response = self.session.get(f"{self.base_url}/transactions/api/budgets/alerts/")
        if response.status_code == 200:
            alerts = response.json()
            print(f"6. Budget Alerts ({len(alerts)} total):")
            for alert in alerts:
                print(f"   - {alert['alert_type']}: {alert['message']} ({alert['spent_percentage']}%)")
        else:
            print(f"6. Budget Alerts - Error: {response.status_code}")
        print()

def main():
    tester = FinancialTrackerAPITest()
    
    print("Attempting to login...")
    if tester.login():
        print("Login successful!\n")
        tester.test_api_endpoints()
    else:
        print("Login failed. Testing public endpoints only...\n")
        # Test public endpoints
        response = requests.get(f"{BASE_URL}/api/")
        print("API Root:")
        print(json.dumps(response.json(), indent=2))
        
        response = requests.get(f"{BASE_URL}/api/docs/")
        print("\nAPI Documentation available at /api/docs/")

if __name__ == "__main__":
    main()