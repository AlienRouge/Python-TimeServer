import requests
import json
from bs4 import BeautifulSoup

server_zone_url = "http://127.0.0.1:8080"
diff_zone_url = server_zone_url + "/Atlantic/Reykjavik"

# GET REQUESTS
# HTML and tag values parsing
print("-GET")
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
# GET Exception: Wrong zone
print("Wrong zone exception: ", requests.get(server_zone_url + "/Tomsk").text)

# POST REQUESTS
print("\n-POST")
print("Post request example: {'date_type': 'time/date/datediff', 'timezones': []}")
print()
_data = {'date_type': 'time'}
print("Server time: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'date'}
print("Server date: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
print()
_data = {'date_type': 'time', 'timezones': ['Asia/Tokyo']}
print("Tokyo time: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'date', 'timezones': ['Asia/Tokyo']}
print("Tokyo date: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
print()
_data = {'date_type': 'datediff', 'timezones': ['Asia/Tomsk', 'Asia/Tokyo']}
print("Tomsk/Tokyo diff: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['Asia/Tokyo', 'Asia/Tomsk']}
print("Tokyo/Tomsk diff: " + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
print()
_data = {'date_type': 'datediff', 'timezones': ['Etc/GMT-14', 'Etc/GMT+12']}
print("UTC-14/UTC+12 diff:" + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu', 'Etc/UTC']}
print("Zulu/UTC diff:" + requests.post(url=server_zone_url, data=json.dumps(_data)).text)
print()
# POST EXCEPTIONS
# JSON Decode Error
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu', 'Etc/UTC']}
print(requests.post(url=server_zone_url, data=_data).text)
print()
# Date_type key not found
_data = {}
print(requests.post(url=server_zone_url, data=json.dumps(_data)).text)
print()
# Timezones type error(list)
_data = {'date_type': 'datediff', 'timezones': 'Etc/Zulu'}
print(requests.post(url=server_zone_url, data=json.dumps(_data)).text)
print()
# Unknown time zone errors
_data = {'date_type': 'time', 'timezones': ['Asia/Tokiyo']}
print(requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['Other/Zulu', 'Etc/UTC']}
print(requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu', 'Etc/GTC']}
print(requests.post(url=server_zone_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu']}
print(requests.post(url=server_zone_url, data=json.dumps(_data)).text)

