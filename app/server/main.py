import json
from typing import List

from fastapi import FastAPI, Request, Body
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel

import pandas as pd


class Expense(BaseModel):
    id: int
    group_id: int | None
    description: str
    cost: str
    currency_code: str
    category: str
    first_name: str
    created_at: str
    updated_at: str


app = FastAPI()

origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173'
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # allow_credentials=True,
    # allow_methods=["*"],
    # allow_headers=["*"],
)


@app.get('/')
def index():
    file = '../pipeline/data/json/January2023.json'
    return json.load(open(file))


@app.get('/expenses/{year}/{month}')
def query_expense_by_month_year(year: int, month: str):
    print('Request received')
    file = f'../pipeline/data/json/{month}{year}.json'
    return json.load(open(file))


# @app.post('/categorized/{year}/{month}')
# async def receive_categorized_expenses(year: int, month: str, request: Request):
#     print(year, month, await request.json())

@app.post('/categorized/{year}/{month}')
async def receive_categorized_expenses(year: int, month: str, expense: List[Expense]):
    print(year, month, expense)
    return {"expense": expense}





