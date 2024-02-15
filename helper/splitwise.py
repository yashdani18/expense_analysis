import requests

from config.keys import API_KEY
from constants.constants import URL_ROOT, ENDPOINT_EXPENSES


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


get_current_user()
