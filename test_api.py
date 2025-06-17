import requests
import json

#testing
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

cross_border_tx = {
    "transaction_id": "tx_cross_border",
    "timestamp": "2025-05-07T14:30:45Z",
    "amount": 150.0,
    "currency": "USD",
    "customer": {"id": "cust1", "country": "US", "ip_address": "192.168.1.1"},
    "payment_method": {"type": "credit_card", "last_four": "5678", "country_of_issue": "CA"},
    "merchant": {"id": "m1", "name": "Electronics Store", "category": "electronics"}
}

high_risk_country_tx = {
    "transaction_id": "tx_high_risk_country",
    "timestamp": "2025-05-07T14:30:45Z",
    "amount": 200.0,
    "currency": "USD",
    "customer": {"id": "cust1", "country": "US", "ip_address": "192.168.1.1"},
    "payment_method": {"type": "credit_card", "last_four": "3456", "country_of_issue": "IR"},  # Iran
    "merchant": {"id": "m1", "name": "Online Store", "category": "electronics"}
}

invalid_tx = {
    "transaction_id": "tx_invalid",
    "timestamp": "2025-05-07T14:30:45Z",
    "amount": 100.0,
    "currency": "USD",
    "payment_method": {"type": "credit_card", "last_four": "7890", "country_of_issue": "US"}
}
def test_webhook(tx_data, expected_action=None):
    response = requests.post(
        "http://localhost:8000/webhook",
        json=tx_data,
        auth=("admin", "secure123")
    )
    print(f"Status: {response.status_code}")
    
    try:
        data = response.json()
        print(f"Response: {json.dumps(data, indent=2)}\n")
        assert "status" in data
        assert "risk_score" in data
        assert "recommended_action" in data
        
        if expected_action:
            assert data["recommended_action"] == expected_action, \
                f"Expected {expected_action} but got {data['recommended_action']}"
            
        return data
    except:
        print(f"Response: {response.text}\n")
        return None
    
print("=== NORMAL TRANSACTION ===")
normal_result = test_webhook(valid_tx, "allow")
if normal_result:
    assert 0 <= normal_result["risk_score"] <= 0.3, \
        "Normal transaction score should be <= 0.3"

print("\n=== HIGH-RISK TRANSACTION ===")
high_risk_result = test_webhook(high_risk_tx, "block")
if high_risk_result:
    assert 0.7 <= high_risk_result["risk_score"] <= 1.0, \
        "High-risk transaction score should be >= 0.7"

print("\n=== ADDITIONAL TESTS ===")



print("=== CROSS-BORDER TRANSACTION ===")
cross_border_result = test_webhook(cross_border_tx, "review")
if cross_border_result:
    assert 0.3 < cross_border_result["risk_score"] <= 0.7, \
        "Cross-border score should be between 0.3-0.7"    
        
print("\n=== HIGH-RISK COUNTRY TRANSACTION ===")
test_webhook(high_risk_country_tx, "block")

print("\n=== INVALID TRANSACTION (MISSING FIELDS) ===")
response = requests.post(
    "http://localhost:8000/webhook",
    json=invalid_tx,
    auth=("admin", "secure123")
)
print(f"Status: {response.status_code} (Expected 400-422)")
print(f"Response: {response.text}\n")
assert response.status_code in [400, 422], "Should fail validation"
        