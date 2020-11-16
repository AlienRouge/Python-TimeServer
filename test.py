import requests
import json
from bs4 import BeautifulSoup

server_url = "http://127.0.0.1:8080"
diff_zone_url = server_url + "/Atlantic/Reykjavik"

# GET REQUESTS
# HTML and tag values parsing
print("-GET")
# Server zone
values = lambda x: [x.find("div", id="timerow").text, x.find("div", id="daterow").text, x.find("div", id="locrow").text]
_html = BeautifulSoup(requests.get(server_url).text, features="html.parser")
print(_html)
print("PARSER: ", values(_html))
# Reykjavik zone
_html = BeautifulSoup(requests.get(diff_zone_url).text, features="html.parser")
print(_html)
print("PARSER: ", values(_html))
# GET Exception: Wrong zone
print("\nWrong zone exception: ", requests.get(server_url + "/Tomsk").text)

# POST REQUESTS
print("\n-POST")
print("Post request example: {'date_type': 'time/date/datediff', 'timezones': []}")
print()
_data = {'date_type': 'time'}
print("Server time: " + requests.post(url=server_url, data=json.dumps(_data)).text)
_data = {'date_type': 'date'}
print("Server date: " + requests.post(url=server_url, data=json.dumps(_data)).text)
print()
_data = {'date_type': 'time', 'timezones': ['America/Argentina/Buenos_Aires']}
print("Buenos_Aires time: " + requests.post(url=server_url, data=json.dumps(_data)).text)
_data = {'date_type': 'date', 'timezones': ['America/Argentina/Buenos_Aires']}
print("Buenos_Aires date: " + requests.post(url=server_url, data=json.dumps(_data)).text)
print()
_data = {'date_type': 'datediff', 'timezones': ['Asia/Tomsk', 'Asia/Shanghai']}
print("Tomsk/Shanghai diff: " + requests.post(url=server_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['Asia/Shanghai', 'Asia/Tomsk']}
print("Shanghai/Tomsk diff: " + requests.post(url=server_url, data=json.dumps(_data)).text)
print()
_data = {'date_type': 'datediff', 'timezones': ['Etc/GMT-14', 'Etc/GMT+12']}
print("UTC-14/UTC+12 diff:" + requests.post(url=server_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['Etc/GMT+12', 'Etc/GMT-14']}
print("UTC+12/UTC-14 diff:" + requests.post(url=server_url, data=json.dumps(_data)).text)
print()
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu', 'Etc/UTC']}
print("Zulu/UTC diff:" + requests.post(url=server_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['UTC', 'UTC']}
print("UTC/UTC diff:" + requests.post(url=server_url, data=json.dumps(_data)).text)
print()
# POST EXCEPTIONS
# JSON Decode Error
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu', 'Etc/UTC']}
print(requests.post(url=server_url, data=_data).text)
print()
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu', 'Etc/UTC']}
print(requests.post(url=server_url, data=None).text)
print()
# Date_type key not found
_data = {}
print(requests.post(url=server_url, data=json.dumps(_data)).text)
print()
# Timezones type error(list)
_data = {'date_type': 'datediff', 'timezones': 'Etc/Zulu'}
print(requests.post(url=server_url, data=json.dumps(_data)).text)
print()
# Time zone errors
# Unknown time zone.
_data = {'date_type': 'time', 'timezones': ['Asia/Buenos_Aires']}
print(requests.post(url=server_url, data=json.dumps(_data)).text)
# First time zone is unknown.
_data = {'date_type': 'datediff', 'timezones': ['Other/Zulu', 'Etc/UTC']}
print(requests.post(url=server_url, data=json.dumps(_data)).text)
# Second time zone is unknown.
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu', 'Etc/GTC']}
print(requests.post(url=server_url, data=json.dumps(_data)).text)
# Incorrect number of elements in "timezones" list. For "datediff" date type - Need(2).
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu']}
print(requests.post(url=server_url, data=json.dumps(_data)).text)
_data = {'date_type': 'datediff', 'timezones': ['Etc/Zulu', 'Etc/UTC', 'Egypt']}
print(requests.post(url=server_url, data=json.dumps(_data)).text)
# "None" in "timezones" argument. For "datediff" expected: list(zone1,zone2).
_data = {'date_type': 'datediff'}
print(requests.post(url=server_url, data=json.dumps(_data)).text)
