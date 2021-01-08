import requests

url = "https://streamlabs.com/api/v1.0/authorize"

response = requests.get(url=url, params="client_id")

print(response.text)

URL = "http://maps.googleapis.com/maps/api/geocode/json"