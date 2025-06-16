import requests
import json

# Test data
valid_tx = {
    "transaction_id": "tx_normal",
    "timestamp": "2025-05-07T14:30:45Z",
    "amount": 50.0,
    "currency": "USD",
    "customer": {"id": "cust1", "country": "US", "ip_address": "192.168.1.1"},
    "payment_method": {"type": "credit_card", "last_four": "1234", "country_of_issue": "US"},
    "merchant": {"id": "m1", "name": "Shop", "category": "books"}
}

high_risk_tx = {
    "transaction_id": "tx_high_risk",
    "timestamp": "2025-05-07T14:30:45Z",
    "amount": 5000.0,
    "currency": "USD",
    "customer": {"id": "cust1", "country": "US", "ip_address": "192.168.1.1"},
    "payment_method": {"type": "credit_card", "last_four": "4321", "country_of_issue": "RU"},
    "merchant": {"id": "m2", "name": "Jewelry", "category": "luxury"}
}

def test_webhook(tx_data):
    response = requests.post(
        "http://localhost:8000/webhook",
        json=tx_data,
        auth=("admin", "secure123")
    )
    print(f"Status: {response.status_code}")
    try:
        print(f"Response: {json.dumps(response.json(), indent=2)}\n")
    except:
        print(f"Response: {response.text}\n")

print("=== NORMAL TRANSACTION ===")
test_webhook(valid_tx)

print("=== HIGH-RISK TRANSACTION ===")
test_webhook(high_risk_tx)