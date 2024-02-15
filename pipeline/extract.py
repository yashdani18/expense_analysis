import json
import pandas as pd
import requests
import time
from config.keys import API_KEY
from constants.constants import ID, GROUP_ID, \
    DESC, COST, CURRENCY_CODE, \
    CATEGORY, CREATED_AT, CREATED_BY, UPDATED_AT, CREATED_BY_ID, CREATED_BY_NAME, CATEGORY_NAME, \
    USER_OWED_SHARE, \
    ARR_MONTHS, DECEMBER, \
    UTF8, NUM_MONTHS, TIME_SLEEP, ID_YASH, LIMIT, USERS, EXPENSES


def get_url(p_limit, p_start_date, p_end_date):
    return f'https://secure.splitwise.com/api/v3.0/get_expenses?limit={p_limit}&dated_after={p_start_date}&dated_before={p_end_date} '


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


years = [2022, 2023]
for year in years:
    lastMonth = False
    path = 'data/' + str(year) + '.csv'
    for month in range(1, NUM_MONTHS + 1, 1):
        start_date = f'{year}{str(month).zfill(2)}01'
        if month == 12:
            year += 1
            month = 1
            lastMonth = True
        else:
            month += 1
        end_date = f'{year}{str(month).zfill(2)}01'
        print(start_date, end_date)
        url = get_url(LIMIT, start_date, end_date)
        response = get_data_from_splitwise(url)
        df = pd.DataFrame(columns=[ID, GROUP_ID, DESC, COST, CURRENCY_CODE,
                                   CATEGORY, CREATED_BY_ID, CREATED_BY_NAME, CREATED_AT, UPDATED_AT])
        expenses = json.loads(response)[EXPENSES]
        for expense in expenses:
            users = expense[USERS]
            for user in users:
                if user['user']['id'] == ID_YASH:
                    new_row = {
                        ID: expense[ID],
                        GROUP_ID: expense[GROUP_ID],
                        DESC: expense[DESC],
                        COST: user[USER_OWED_SHARE],
                        CURRENCY_CODE: expense[CURRENCY_CODE],
                        CATEGORY: expense[CATEGORY][CATEGORY_NAME],
                        CREATED_BY_ID: expense[CREATED_BY][CREATED_BY_ID],
                        CREATED_BY_NAME: expense[CREATED_BY][CREATED_BY_NAME],
                        CREATED_AT: expense[CREATED_AT],
                        UPDATED_AT: expense[UPDATED_AT]}
                    df.loc[len(df)] = new_row

        # df.to_excel(writer, sheet_name=(
        #     ARR_MONTHS[month - 1] + str(year) if lastMonth is False else (DECEMBER + str(year - 1))), encoding=UTF8)
        df.to_csv('data/' + (ARR_MONTHS[month - 1] + str(year) + '.csv') if lastMonth is False
                  else 'data/' + (DECEMBER + str(year - 1) + '.csv'),
                  encoding=UTF8)
        # df.to_excel('records/' + ARR_MONTHS[month - 1] + str(year) + ".csv", sep='\t', encoding='utf-8')
        time.sleep(TIME_SLEEP)
    # df
