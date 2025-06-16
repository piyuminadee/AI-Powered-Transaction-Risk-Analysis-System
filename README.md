# Transaction Risk Analysis System

## Setup
1. Create `.env` file:

2. Install dependencies: `pip install -r requirements.txt`
3. Run: `uvicorn app.main:app --reload`

## Testing
- Use `test_api.py`: `python test_api.py`
- Or send POST requests to `http://localhost:8000/webhook`

## Endpoints
POST `/webhook`
- Basic auth required
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