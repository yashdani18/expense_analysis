import json

import requests

response = requests.get('http://localhost:8000').text
print(type(response))

expenses = json.loads(response)
for expense in expenses:
    print(expense['description'])

