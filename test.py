import requests
import json
from bs4 import BeautifulSoup

server_zone_url = "http://127.0.0.1:8080"
diff_zone_url = server_zone_url + "/Atlantic/Reykjavik"

# GET REQUESTS
print("GET")
# Server zone
_html = BeautifulSoup(requests.get(server_zone_url).text, features="html.parser")
print(_html)
html_parser = [_html.find("div", id="timerow").text, _html.find("div", id="header").text]
print("PARSER: ", html_parser)
# Reykjavik zone
_html = BeautifulSoup(requests.get(diff_zone_url).text, features="html.parser")
print(_html)
html_parser = [_html.find("div", id="timerow").text, _html.find("div", id="header").text]
print("PARSER: ", html_parser)
# Wrong zone
print(requests.get(server_zone_url + "/Tomsk").text)

# POST REQUESTS
print("\nPOST")
print("Post request example: {'date_type': 'time/date/datediff', 'timezones': []}")

_data = {'date_type': 'time'}
print("Server time: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'date'}
print("Server date: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)

print()

_data = {'date_type': 'time', 'timezones': ['Asia/Tokyo','Asia/Tokyo','Asia/Tokyo','Asia/Tokyo','Asia/Tokyo', 'Asia/Tokyo']}
print("Tokyo time: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'date', 'timezones': ['Asia/Tokyo']}
print("Tokyo date: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)

_data = {'date_type': 'datediff', 'timezones': ['Asia/Tomsk', 'Asia/Tokyo']}
print("Tomsk/Tokyo diff: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['Asia/Tokyo', 'Asia/Tomsk']}
print("Tokyo/Tomsk diff: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)


_data = {'date_type': 'datediff', 'timezones': ['Etc/GMT-12', 'Etc/GMT+12']}
print("1: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)