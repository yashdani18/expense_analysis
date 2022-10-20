import requests
import keys
import pprint

pp = pprint.PrettyPrinter(indent=4)

response = requests.get('https://secure.splitwise.com/api/v3.0/get_printable_summary?group_id=30109179&date=2022-06',
                        headers={'Authorization': 'Bearer ' + keys.api_key}).text

pp.pprint(response)
