import requests

url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Washington%2C%20DC&destinations=New%20York%20City%2C%20NY&units=imperial&key=AIzaSyC5kyx-qrinNKt_RBLzdyzi_KGiPCnuwO0"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)