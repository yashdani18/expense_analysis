import json
import math
import time
import os
from datetime import datetime

from pprint import pprint

import pandas as pd

from constants.constants import ID, EXPENSE_ID, GROUP_ID, GROUP_NAME, \
    DESC, COST, CURRENCY_CODE, \
    CATEGORY, \
    CREATED_AT, UPDATED_AT, CREATED_BY, UPDATED_BY, DELETED_AT, DELETED_BY, DELETED_BY, \
    USER_ID, USER_FIRST_NAME, USER_LAST_NAME, \
    REPAYMENTS, REPAYMENTS_FROM, REPAYMENTS_TO, REPAYMENTS_AMOUNT, \
    USERS, USER_PAID_SHARE, USER_OWED_SHARE, USER_NET_BALANCE

from helper.splitwise import get_user, get_group

from config.db import HOST, USER, PASSWORD, DATABASE

import mysql.connector


# Global variables
set_db_user_ids = set()
set_db_group_ids = set()

new_user_ids = set()
new_group_ids = set()

users = []
groups = []
user_groups = []
expenses = []
repayments = []
shares = []


def connect_db():
    temp_db = mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )
    temp_cursor = temp_db.cursor()
    return temp_db, temp_cursor


def disconnect_db(p_db, p_cursor):
    p_cursor.close()
    p_db.close()


def fetch_db_user_ids(p_cursor):
    p_cursor.execute('SELECT user_id FROM users')
    cursor_users = p_cursor.fetchall()

    for cursor_user in cursor_users:
        set_db_user_ids.add(cursor_user[0])


def fetch_db_group_ids(p_cursor):
    p_cursor.execute('SELECT group_id FROM exp_groups')
    cursor_groups = p_cursor.fetchall()

    for cursor_group in cursor_groups:
        set_db_group_ids.add(cursor_group[0])


def isDeleted(p_expense):
    return p_expense[DELETED_AT] is not None


def isNonGroupExpense(p_expense):
    return p_expense[GROUP_ID] == 0


def appendExpenses(p_expense):
    expenses.append({
        EXPENSE_ID: p_expense[EXPENSE_ID],
        GROUP_ID: p_expense[GROUP_ID],
        DESC: p_expense[DESC],
        COST: p_expense[COST],
        CREATED_BY: p_expense[CREATED_BY],
        CREATED_AT: p_expense[CREATED_AT],
        UPDATED_BY: p_expense[UPDATED_BY],
        UPDATED_AT: p_expense[UPDATED_AT],
    })


def appendShares(p_expense):
    for temp_user in p_expense[USERS]:
        shares.append({
            USER_ID: temp_user[USER_ID],
            EXPENSE_ID: p_expense[EXPENSE_ID],
            GROUP_ID: p_expense[GROUP_ID],
            USER_PAID_SHARE: temp_user[USER_PAID_SHARE],
            USER_OWED_SHARE: temp_user[USER_OWED_SHARE],
            USER_NET_BALANCE: temp_user[USER_NET_BALANCE]
        })


def appendRepayments(p_expense):
    for repayment in p_expense[REPAYMENTS]:
        repayments.append({
            EXPENSE_ID: p_expense[EXPENSE_ID],
            GROUP_ID: p_expense[GROUP_ID],
            REPAYMENTS_FROM: repayment[REPAYMENTS_FROM],
            REPAYMENTS_TO: repayment[REPAYMENTS_TO],
            REPAYMENTS_AMOUNT: float(repayment[REPAYMENTS_AMOUNT])
        })


def load(source_file):
    arr_expenses = json.load(open(source_file))

    for expense in arr_expenses:
        if isDeleted(expense):
            continue

        if expense[EXPENSE_ID] == 1532519262:
            continue

        if expense[GROUP_ID] not in set_db_group_ids:
            new_group_ids.add(expense[GROUP_ID])

        appendExpenses(expense)

        appendShares(expense)

        # if isNonGroupExpense(expense):
        #     continue

        appendRepayments(expense)


def updateUsersGroups():
    for new_group_id in new_group_ids:
        response = json.loads(get_group(int(new_group_id)))['group']
        new_group = {
            GROUP_ID: response[ID],
            GROUP_NAME: response['name']
        }
        groups.append(new_group)
        members = response['members']
        for member in members:
            member_id = member[ID]
            user_groups.append({
                USER_ID: member_id,
                GROUP_ID: response[ID]
            })
            if member_id not in set_db_user_ids:
                # new_user_ids.add(member_id)
                users.append({
                    USER_ID: member[ID],
                    USER_FIRST_NAME: member[USER_FIRST_NAME],
                    USER_LAST_NAME: member[USER_LAST_NAME]
                })
                set_db_user_ids.add(member_id)


def insert_into_mysql(p_db, p_cursor):
    for user in users:
        sql = f'REPLACE INTO users({USER_ID}, {USER_FIRST_NAME}, {USER_LAST_NAME}) VALUES (%s, %s, %s)'
        val = (user[USER_ID], user[USER_FIRST_NAME], user[USER_LAST_NAME])
        p_cursor.execute(sql, val)

    time.sleep(1)

    for group in groups:
        sql = f'REPLACE INTO exp_groups({GROUP_ID}, {GROUP_NAME}) VALUES (%s, %s)'
        val = (group[GROUP_ID], group[GROUP_NAME])
        p_cursor.execute(sql, val)

    time.sleep(1)

    for user_group in user_groups:
        sql = f'REPLACE INTO users_groups({USER_ID}, {GROUP_ID}) VALUES (%s, %s)'
        val = (user_group[USER_ID], user_group[GROUP_ID])
        p_cursor.execute(sql, val)

    time.sleep(1)

    for expense in expenses:
        try:
            sql = f'REPLACE INTO expenses' \
                  f'({EXPENSE_ID}, {GROUP_ID}, {DESC}, {COST}, {CREATED_BY}, {CREATED_AT}, {UPDATED_BY}, {UPDATED_AT}) ' \
                  f'VALUES (%s, %s, %s, %s, %s, %s, %s, %s) '
            val = (expense[EXPENSE_ID], expense[GROUP_ID],
                   expense[DESC], expense[COST],
                   expense[CREATED_BY], datetime.strptime(expense[CREATED_AT], '%Y-%m-%dT%H:%M:%SZ'),
                   expense[UPDATED_BY], datetime.strptime(expense[UPDATED_AT], '%Y-%m-%dT%H:%M:%SZ'))
            p_cursor.execute(sql, val)
        except:
            print(expense[EXPENSE_ID])
            exit(1)

    time.sleep(1)

    for repayment in repayments:
        sql = f'REPLACE INTO repayments' \
              f'({EXPENSE_ID}, {GROUP_ID}, user_from, user_to, {REPAYMENTS_AMOUNT}) ' \
              f'VALUES (%s, %s, %s, %s, %s)'
        val = (repayment[EXPENSE_ID], repayment[GROUP_ID],
               repayment[REPAYMENTS_FROM], repayment[REPAYMENTS_TO],
               repayment[REPAYMENTS_AMOUNT])
        p_cursor.execute(sql, val)

    time.sleep(1)

    for share in shares:
        sql = f'REPLACE INTO shares' \
              f'({USER_ID}, {EXPENSE_ID}, {GROUP_ID}, {USER_PAID_SHARE}, {USER_OWED_SHARE}, {USER_NET_BALANCE}) ' \
              f'VALUES (%s, %s, %s, %s, %s, %s)'
        val = (share[USER_ID], share[EXPENSE_ID], share[GROUP_ID],
               share[USER_PAID_SHARE], share[USER_OWED_SHARE],
               share[USER_NET_BALANCE])
        p_cursor.execute(sql, val)

    time.sleep(1)

    p_db.commit()


def insert_into_csv():

    df = pd.DataFrame(users)
    # print(df)
    df.to_csv('data/csv/users.csv', index=False)

    df = pd.DataFrame(groups)
    # print(df)
    df.to_csv('data/csv/groups.csv', index=False)

    df = pd.DataFrame(user_groups)
    # print(df)
    df.to_csv('data/csv/users_groups.csv', index=False)

    df = pd.DataFrame(expenses)
    # print(df)
    df.to_csv('data/csv/expenses.csv', index=False)

    df = pd.DataFrame(repayments)
    # print(df)
    df.to_csv('data/csv/repayments.csv', index=False)

    df = pd.DataFrame(shares)
    # print(df)
    df.to_csv('data/csv/shares.csv', index=False)


if __name__ == "__main__":
    print('Load starting...')

    # Housekeeping
    db, cursor = connect_db()
    fetch_db_user_ids(cursor)
    fetch_db_group_ids(cursor)

    # loading extracted data into MySQL tables
    directory = 'data/json/'
    files = os.listdir(directory)

    for file in files:
        print('Processing: ', (directory + file) + '...')
        load(directory + file)
        time.sleep(1)

    updateUsersGroups()
    print('Inserting data into MySQL...')
    insert_into_mysql(db, cursor)
    print('Inserting data into CSV files...')
    insert_into_csv()

    disconnect_db(db, cursor)
