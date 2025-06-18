# Transaction Risk Analysis System

## Setup
1. Create `.env` file: with the following variables:
- DEEPSEEK_API_KEY="key here"
- WEBHOOK_USER="admin"
- WEBHOOK_PASS="secure123"

2. Install dependencies: `pip install -r requirements.txt`
3. Run: `uvicorn app.main:app --reload`

## Testing
- Use `test_api.py`: `python test_api.py`
- Or send POST requests to `http://localhost:8000/webhook`

## Endpoints
POST `/webhook`
- Basic auth required (Authentication: Basic Authentication (set in .env))
- Response: Transaction ID, risk score, and recommended action
- JSON body format:
```json
{
 "transaction_id": "...",
 "timestamp": "...",
 ...
}


## Test Cases
| Type                  | Risk Score | Action  |
|-----------------------|------------|---------|
| Normal                | 0.0-0.3    | allow   |
| Cross-Border          | 0.3-0.7    | review  |
| High-Risk Country (RU)| 0.7-1.0    | block   |


## Test for high risk transaction
{
  "transaction_id": "tx_high_risk_country",
  "timestamp": "2025-05-07T14:30:45Z",
  "amount": 200.0,
  "currency": "USD",
  "customer": {
    "id": "cust1",
    "country": "US",
    "ip_address": "192.168.1.1"
  },
  "payment_method": {
    "type": "credit_card",
    "last_four": "3456",
    "country_of_issue": "RU"
  },
  "merchant": {
    "id": "m1",
    "name": "Online Store",
    "category": "electronics"
  }
}