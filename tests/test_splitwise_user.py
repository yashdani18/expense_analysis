import json

import helper.splitwise as source
from constants.constants import USER, USER_FIRST_NAME


def test_user():
    response = source.get_current_user()
    expenses = json.loads(response)[USER]
    assert expenses[USER_FIRST_NAME] == 'yashdani'

