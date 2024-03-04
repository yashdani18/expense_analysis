import json

import helper.splitwise as source
from constants.constants import USER, USER_FIRST_NAME


def test_user():
    response = source.get_current_user()
    expenses = json.loads(response)[USER]
    assert expenses[USER_FIRST_NAME] == 'yashdani'


def test_expense():
    response = source.get_data_from_splitwise(source.get_expenses_url(p_limit=1, p_start_date='20230114', p_end_date='20230115'))
    print(response)


test_expense()
