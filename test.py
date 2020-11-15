import requests
import json
from bs4 import BeautifulSoup

server_zone_url = "http://127.0.0.1:8080"
diff_zone_url = server_zone_url + "Atlantic/Reykjavik"

# # GET REQUESTS
# print("GET")
# # Server zone
# _html = BeautifulSoup(requests.get(server_zone_url).text, features="html.parser")
# parser = [_html.find("div", id="timerow").text, _html.find("div", id="header").text]
# print(parser)
# # Reykjavik zone
# _html = BeautifulSoup(requests.get(diff_zone_url).text, features="html.parser")
# parser = [_html.find("div", id="timerow").text, _html.find("div", id="header").text]
# print(parser)
# # Wrong zone
# print(requests.get(server_zone_url + "/Tomsk").text)

# POST REQUESTS
print("\nPOST")
_data = {'date_type': 'datediff','timezones': ['Asia/Tomsk','Europe/Moscow']}
print(requests.post(url=server_zone_url, data=json.dumps(_data)).text)
