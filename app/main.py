from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import httpx
import os
import json
from dotenv import load_dotenv
from .schemas import Transaction, RiskAnalysis

# Load environment variables
load_dotenv()

app = FastAPI()
security = HTTPBasic()

# Basic authentication
def verify_credentials(credentials: HTTPBasicCredentials):
    return (
        credentials.username == os.getenv("WEBHOOK_USER") and
        credentials.password == os.getenv("WEBHOOK_PASS")
    )

def analyze_with_deepseek(transaction: dict) -> RiskAnalysis:
    """Analyze transaction using DeepSeek API"""
    prompt = f"""
    [SYSTEM] You are a financial risk analyst. Analyze this transaction and follow these rules EXACTLY:
    1. Risk score MUST be between 0.0-1.0
    2. Recommended action MUST be:
        - "allow" if risk_score <= 0.3
        - "review" if 0.3 < risk_score <= 0.7
        - "block" if risk_score > 0.7
    3. Consider these risk factors:
        - Geographic mismatch (customer vs payment country)
        - High-risk countries (RU, IR, KP, VE, MM)
        - Unusual transaction amount
        - Suspicious timing/patterns
        
        Respond ONLY in this JSON format:
    {{
        "risk_score": number,
        "risk_factors": ["factor1", "factor2"],
        "reasoning": "string",
        "recommended_action": "allow|review|block"
    }}

    Transaction data:
    {json.dumps(transaction, indent=2)}
    """
    
    headers = {
        "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-chat",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.1,
        "response_format": {"type": "json_object"}
    }
    
    try:
        response = httpx.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=30
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return RiskAnalysis(**json.loads(content))
    except Exception as e:
        raise HTTPException(500, f"DeepSeek API error: {str(e)}")

@app.post("/webhook")
async def process_transaction(
    transaction: Transaction,
    credentials: HTTPBasicCredentials = Depends(security)
):
    # Verify credentials
    if not verify_credentials(credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Basic"},
        )
    
    # Convert to dict for DeepSeek
    tx_dict = transaction.dict()
    
    # Get risk analysis
    try:
        risk_data = analyze_with_deepseek(tx_dict)
    except HTTPException as e:
        return {"error": str(e)}
    
   
    if risk_data.risk_score >= 0.7:
        alert = {
            "alert_type": "high_risk_transaction",
            "transaction_id": transaction.transaction_id,
            "risk_score": risk_data.risk_score,
            "risk_factors": risk_data.risk_factors,
            "transaction_details": transaction.dict(),
            "llm_analysis": risk_data.reasoning
        }
        print(f" ADMIN ALERT: {json.dumps(alert, indent=2)}")
    
    return {
        "status": "processed",
        "risk_score": risk_data.risk_score,
        "recommended_action": risk_data.recommended_action
    }