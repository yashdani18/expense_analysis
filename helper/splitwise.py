import json

import requests

import constants.constants
from config.keys import API_KEY
from constants.constants import URL_ROOT, ENDPOINT_EXPENSES, USERS


def get_url(endpoint):
    return f'{URL_ROOT}/{endpoint}'


def get_expenses_url(p_limit, p_start_date, p_end_date):
    return f'{URL_ROOT}/{ENDPOINT_EXPENSES}?limit={p_limit}&dated_after={p_start_date}&dated_before={p_end_date}'


def get_data_from_splitwise(p_url):
    response = requests.get(p_url, headers={
        'Authorization': f'Bearer {API_KEY}',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 '
                      'Safari/537.36',
        "Upgrade-Insecure-Requests": "1",
        "DNT": "1",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate"}).text
    return response


def get_current_user():
    url = get_url('get_current_user')
    response = get_data_from_splitwise(url)
    return response


def get_user(user_id):
    url = get_url(f'get_user/{user_id}')
    response = get_data_from_splitwise(url)
    return response


def get_group(group_id):
    url = get_url(f'get_group/{group_id}')
    response = get_data_from_splitwise(url)
    return response


def get_groups():
    url = get_url('get_groups')
    response = get_data_from_splitwise(url)
    return response


def get_categories():
    url = get_url('get_categories')
    response = get_data_from_splitwise(url)
    return response


def get_expenses_jan_2023():
    url = get_expenses_url(1000, 20230101, 20230201)
    response = get_data_from_splitwise(url)
    expenses = json.loads(response)['expenses']

    cost = 0

    for expense in expenses:
        users = expense[USERS]
        for user in users:
            if user[constants.constants.USER_ID] == constants.constants.ID_YASH and \
                    expense[constants.constants.DELETED_AT] is None:
                cost += float(user[constants.constants.USER_OWED_SHARE])

    print(cost)


def get_expense(expense_id):
    url = get_url(f'get_expense/{expense_id}')
    response = get_data_from_splitwise(url)
    return response


# get_current_user()

# print(get_groups())

if __name__ == "__main__":
    # print(get_categories())

    # print(get_user('46379417'))

    # print(get_group(23291838))

    # get_expenses_jan_2023()

    print(get_expense(1532519262))
