import requests
from pprint import pprint
# from utils import write_json

# url = 'https://prod-public-api.livescore.com/v1/api/app/live/soccer/7?locale=en&MD=1'
# url = 'http://api.kingbets360.com:5002/api/v1/match-result'
url = 'https://www.livescore.com/_next/data/C7Y8bolW0SuDOOqgNeT2V/en/football/euro-2024/semi-finals/spain-vs-france/1274137.json'
res = requests.get(url)
# print(res.status_code)
pprint(res.json())
# write_json(res.json(), './tmp/test.json')