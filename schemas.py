from pydantic import BaseModel

class BusinessHealthRequest(BaseModel):
    sales: int
    expenses: int
    profit: int