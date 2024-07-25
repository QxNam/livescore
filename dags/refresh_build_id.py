import requests
from utils import write_json, read_json
from pprint import pprint

path = './tmp/build_id.json'
build_id = read_json(path)
url=f'https://www.livescore.com/_next/data/{build_id["build_id"]}/en/football/euro-2024/semi-finals/spain-vs-france/1274137.json'

def refresh():
    try:
        print(url)
        res = requests.get(url)
        pprint(res.json())
        build_id = res.json()['pageProps']['__N_REDIRECT'].split('buildid=')[-1]
        data = {'build_id': build_id}
        write_json(data, path)
    except:
        pass