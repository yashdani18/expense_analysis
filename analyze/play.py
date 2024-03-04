import pandas as pd
import os

from helper.splitwise import get_data_from_splitwise, get_expenses_url

print(get_data_from_splitwise(get_expenses_url(1000, '20231201', '20240101')))
exit(0)

directory_path = "../pipeline/data"
files = os.listdir(directory_path)

categories = ['1.Fruits', '2.Vegetables', '3.Groceries', '4.Dining Out', '5.Home Care', '6.Personal Care', '7.Snacks']

for file in files:
    filename = f'{directory_path}/{file}'
    df = pd.read_csv(filename)
    print(file, len(df))
    for index, row in df.iterrows():
        print(f"{row['description']}\t{row['cost']}")
        # print(categories)
        val = input(categories)
    break