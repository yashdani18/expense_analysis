import pandas as pd

df = pd.read_csv('data/csv/raw_january_2023.csv')

# print(df.info())
# df.info() prints dtype of a value, not the type

# transformation starts here
if type(df['created_at'].loc[0]) is str:
    df['created_at'] = pd.to_datetime(df['created_at']).apply(lambda x: x.date())


if type(df['updated_at'].loc[0]) is str:
    df['updated_at'] = pd.to_datetime(df['updated_at']).apply(lambda x: x.date())

# transformation ends here

# print(df.info())

df.to_csv('data/csv/transformed_january_2023.csv', index=False)
