from pipeline.extract import get_data_from_splitwise

url = f'https://secure.splitwise.com/api/v3.0/get_expenses?limit=10&dated_after=20231215&dated_before=20231218'
print(get_data_from_splitwise(url))
