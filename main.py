import json

import requests

import Constants
import keys
import pprint

pp = pprint.PrettyPrinter(indent=4)

response = requests.get('https://secure.splitwise.com/api/v3.0/get_expenses?limit=20&dated_after=20221001&dated_before=20221021T0000', headers={
    'Authorization': 'Bearer ' + keys.api_key
}).text

total_expense = 0
total_paid = 0

results = json.loads(response)
print(results)
expenses = results['expenses']
for index, expense in enumerate(expenses):
    created_at = expense[Constants.CREATED_AT]
    item = expense[Constants.DESC]
    cost = expense[Constants.COST]
    group_id = expense[Constants.GROUP_ID]
    if group_id is None:
        # Personal expenses (Non-group)
        expense_amount = cost
        # total_expense += float(cost)
        total_paid += float(cost)
        print(created_at, item, cost, expense_amount, total_expense)
        continue
    users = expense['users']
    for user in users:
        if user[Constants.USER][Constants.USER_ID] == Constants.YASH_ID:
            expense_amount = float(user[Constants.USER_OWED_SHARE])
            total_expense += expense_amount
            total_paid += float(user[Constants.USER_PAID_SHARE])
            print(created_at, item, cost, expense_amount, total_expense)
            break

    # if item == 'Rice':
    # print('expense amount', expense_amount)
    # print('total amount', total_expense)
    # print(expense['description'])
    # pp.pprint(expense)
