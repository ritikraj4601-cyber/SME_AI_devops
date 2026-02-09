from pydantic import BaseModel

class BusinessHealthRequest(BaseModel):
    sales: float
    expenses: float
    profit: float