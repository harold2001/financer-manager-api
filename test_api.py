"""
Example script demonstrating how to use the Personal Finance Manager API

This script shows how to:
1. Register a new user
2. Create transactions
3. Retrieve and filter transactions
4. Update and delete transactions

Note: You'll need to implement client-side Firebase auth for production use.
This is just for testing the API endpoints.
"""

import requests
import json
from datetime import datetime

BASE_URL = "http://localhost:8000"


def test_api():
    """Test the Personal Finance Manager API"""

    print("🚀 Testing Personal Finance Manager API")
    print("=" * 50)

    # Test root endpoint
    print("\n1. Testing root endpoint...")
    response = requests.get(f"{BASE_URL}/", timeout=1000)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")

    # Test user registration
    print("\n2. Testing user registration...")
    user_data = {
        "email": "test@example.com",
        "password": "testpassword123",
        "name": "Test User",
    }

    response = requests.post(f"{BASE_URL}/auth/register", json=user_data, timeout=1000)
    print(f"Status: {response.status_code}")

    if response.status_code == 201:
        auth_response = response.json()
        print("Registration successful!")
        print(f"User ID: {auth_response['user']['id']}")
        token = auth_response["token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Test user profile
        print("\n3. Testing user profile...")
        response = requests.get(f"{BASE_URL}/users/me", headers=headers, timeout=1000)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print(f"User profile: {json.dumps(response.json(), indent=2)}")

        # Test creating transactions
        print("\n4. Testing transaction creation...")
        transactions = [
            {
                "type": "income",
                "amount": 5000.0,
                "category": "salary",
                "date": datetime.now().isoformat(),
                "description": "Monthly salary",
            },
            {
                "type": "expense",
                "amount": 50.0,
                "category": "food",
                "date": datetime.now().isoformat(),
                "description": "Grocery shopping",
            },
            {
                "type": "expense",
                "amount": 30.0,
                "category": "transport",
                "date": datetime.now().isoformat(),
                "description": "Gas",
            },
        ]

        created_transactions = []
        for tx_data in transactions:
            response = requests.post(
                f"{BASE_URL}/transactions/", json=tx_data, headers=headers, timeout=1000
            )
            print(f"Creating transaction: Status {response.status_code}")
            if response.status_code == 201:
                created_transactions.append(response.json())

        # Test getting all transactions
        print("\n5. Testing get all transactions...")
        response = requests.get(
            f"{BASE_URL}/transactions/", headers=headers, timeout=1000
        )
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            all_transactions = response.json()
            print(f"Total transactions: {len(all_transactions)}")

        # Test filtering transactions
        print("\n6. Testing transaction filtering...")
        response = requests.get(
            f"{BASE_URL}/transactions/?type=expense", headers=headers, timeout=1000
        )
        print(f"Expense transactions: Status {response.status_code}")
        if response.status_code == 200:
            expense_transactions = response.json()
            print(f"Expense transactions count: {len(expense_transactions)}")

        # Test updating a transaction
        if created_transactions:
            print("\n7. Testing transaction update...")
            transaction_id = created_transactions[0]["id"]
            update_data = {"description": "Updated description"}
            response = requests.put(
                f"{BASE_URL}/transactions/{transaction_id}",
                json=update_data,
                headers=headers,
                timeout=1000,
            )
            print(f"Update transaction: Status {response.status_code}")

        print("\n✅ API testing completed!")

    else:
        print(f"Registration failed: {response.text}")


if __name__ == "__main__":
    test_api()
