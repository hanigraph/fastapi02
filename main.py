from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, condecimal, conint
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title='Student loan payments',
    version='MOTOPP 0.1'
   )

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request model with additional validation
class LoanRequest(BaseModel):
    age: conint(ge=18, le=30)  # type: ignore # Age must be between 18 and 30
    loan_amount: condecimal(ge=1000, le=50000, max_digits=7, decimal_places=2)  # type: ignore # Loan amount must be between 1000 and 500000
    years_to_repay: conint(ge=1, le=20)  # type: ignore # Years to repay must be between 1 and 20
    interest_rate: condecimal(ge=0, le=10, max_digits=4, decimal_places=2) = 5.0  # type: ignore # Interest rate must be between 0 and 10

# Helper function to calculate monthly payment
def calculate_monthly_payment(loan_amount: float, annual_interest_rate: float, years: int) -> float:
    monthly_interest_rate = annual_interest_rate / 100 / 12
    number_of_payments = years * 12
    if monthly_interest_rate == 0:
        return loan_amount / number_of_payments
    return loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)

@app.post("/calculate_loan/")
def calculate_loan(request: LoanRequest):
    try:
        # The validation constraints will automatically raise validation errors if inputs are invalid
        # Calculate monthly payment
        monthly_payment = calculate_monthly_payment(
            request.loan_amount,
            request.interest_rate,
            request.years_to_repay
        )
        return {"monthly_payment": monthly_payment}
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Value error: {str(e)}")
    except TypeError as e:
        raise HTTPException(status_code=400, detail=f"Type error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Run the app using: uvicorn main:app --reload
#Hello World000000
