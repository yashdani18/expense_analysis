import json
import requests
import time
from config.keys import API_KEY
from constants.constants import ID, GROUP_ID, \
    DESC, COST, CURRENCY_CODE, \
    CATEGORY, CREATED_AT, CREATED_BY, UPDATED_AT, CATEGORY_NAME, \
    UPDATED_BY, \
    DELETED_BY, DELETED_AT, \
    USER_OWED_SHARE, \
    ARR_MONTHS, DECEMBER, \
    NUM_MONTHS, TIME_SLEEP, LIMIT, USERS, EXPENSES, EXPENSE_ID, \
    REPAYMENTS, USER_ID

from helper.splitwise import get_expenses_url, get_data_from_splitwise


def extract():
    total = 0
    years = [2022, 2023]
    for year in years:
        lastMonth = False
        for month in range(1, NUM_MONTHS + 1, 1):
            start_date = f'{year}{str(month).zfill(2)}01'
            if month == 12:
                year += 1
                month = 1
                lastMonth = True
            else:
                month += 1
            end_date = f'{year}{str(month).zfill(2)}01'
            url = get_expenses_url(LIMIT, start_date, end_date)
            response = get_data_from_splitwise(url)
            expenses = json.loads(response)[EXPENSES]
            arr_expenses = []
            for expense in expenses:

                if expense[ID] == 1532519262 or expense[DESC] == 'Payment' or expense[DESC] == 'Settle all balances':
                    continue

                #
                users = expense[USERS]
                for user in users:
                    if user[USER_ID] == 32703372 and expense[DELETED_AT] is None:
                        total += float(user[USER_OWED_SHARE])
                #

                new_row = {
                    EXPENSE_ID: expense[ID],
                    GROUP_ID: expense[GROUP_ID] if expense[GROUP_ID] is not None else 0,
                    DESC: expense[DESC],
                    COST: expense[COST],
                    CURRENCY_CODE: expense[CURRENCY_CODE],
                    CATEGORY: expense[CATEGORY][CATEGORY_NAME],
                    CREATED_BY: expense[CREATED_BY][ID],
                    CREATED_AT: expense[CREATED_AT],
                    UPDATED_BY: expense[UPDATED_BY][ID] if expense[UPDATED_BY] is not None else 0,
                    UPDATED_AT: expense[UPDATED_AT],
                    DELETED_BY: expense[DELETED_BY][ID] if expense[DELETED_BY] is not None else 0,
                    DELETED_AT: expense[DELETED_AT],
                    REPAYMENTS: expense[REPAYMENTS],
                    USERS: expense[USERS]
                }
                arr_expenses.append(new_row)
            filename = f'data/json/raw_{ARR_MONTHS[month - 1]}_{str(year)}.json' if lastMonth is False \
                else f'data/json/raw_{DECEMBER}_{str(year - 1)}.json'
            print('Writing to', filename, '...')
            with open(filename, "w") as f:
                json.dump(arr_expenses, f)
            time.sleep(TIME_SLEEP)
        # df
    print(total)


extract()
