from pydantic import BaseModel

class Customer(BaseModel):
    id: str
    country: str
    ip_address: str

class PaymentMethod(BaseModel):
    type: str
    last_four: str
    country_of_issue: str

class Merchant(BaseModel):
    id: str
    name: str
    category: str

class Transaction(BaseModel):
    transaction_id: str
    timestamp: str
    amount: float
    currency: str
    customer: Customer
    payment_method: PaymentMethod
    merchant: Merchant

class RiskAnalysis(BaseModel):
    risk_score: float
    risk_factors: list[str]
    reasoning: str
    recommended_action: str