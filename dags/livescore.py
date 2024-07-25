import requests, json
from datetime import datetime
from cosine import the_nearest
from utils import *

# --- init base ---
build_id = read_json('./tmp/build_id.json')
url = 'https://www.livescore.com/_next/data/{build_id}/en/football/{cmnt}/{scd}/{t1}-vs-{t2}/{eid}.json'
url_live = 'https://prod-public-api.livescore.com/v1/api/app/live/soccer/7?locale=en&MD=1'
# url_live = 'https://prod-public-api.livescore.com/v1/api/app/stage/soccer/usa/major-league-soccer/7?locale=en&MD=1'
# pageProps
DATA = {
    'tournament': 'categoryName',
    'home_team': 'homeTeamName',
    'away_team': 'awayTeamName',
    # 'period': 'scores.statusInt', # str
    'period': 'incidents.incs', # len(key)
}

# --- functions ---
def _collect_data(data, key_str):
    res = data.copy()
    keys = key_str.split('.')
    try:
        for key in keys:
            res = res.get(key)
        return res
    except:
        return None

def get_stage(match_target):
    datas = {}
    response = requests.get(url_live)
    competitions = response.json()['Stages']
    for competition in competitions:
        cnm = competition['Cnm']
        cmnt = competition['CnmT']
        scd = competition['Scd']
        for game in competition['Events']:
            eid = game['Eid']
            t1 = game['T1'][0]['Nm'].lower().replace(' ', '-').replace('/', '_').replace("'", '')
            t2 = game['T2'][0]['Nm'].lower().replace(' ', '-').replace('/', '_').replace("'", '')
            datas[f'{cnm}-{t1}-{t2}'] = url.format(build_id=build_id['build_id'], cmnt=cmnt, scd=scd, t1=t1, t2=t2, eid=eid)
    # value, target_best, score = the_nearest(datas, match_target)
    return the_nearest(datas, match_target)

def get_score(url='https://www.livescore.com/_next/data/LbC2S31VjzszcKPHb0uaY/en/football/euro-2024/semi-finals/spain-vs-france/1274137.json'):
    data = {}
    response = requests.get(url)
    data_json = response.json()['pageProps']['initialEventData']['event']
    for key, value in DATA.items():
        data[key] = _collect_data(data_json, value)
    try:
        data['period'] = len(data['period'])
    except:
        data['period'] = 1
    # print(data['period'])
    temp_score = {}
    if data['period']==1:
        temp_score['home_team'] = int(_collect_data(data_json, 'scores.homeTeamScore'))
        temp_score['away_team'] = int(_collect_data(data_json, 'scores.awayTeamScore'))
        data['firsthalf_score'] = temp_score
        data['fulltime_score'] = temp_score
    else:
        ht_score = data_json['scores']['scoresByPeriod'][0]
        temp_score['home_team'] = int(_collect_data(ht_score, 'home.score'))
        temp_score['away_team'] = int(_collect_data(ht_score, 'away.score'))
        data['firsthalf_score'] = temp_score
        
    temp_score['home_team'] = int(_collect_data(data_json, 'scores.homeTeamScore'))
    temp_score['away_team'] = int(_collect_data(data_json, 'scores.awayTeamScore'))
    data['fulltime_score'] = temp_score
        
    return data

def fetch_livescore_data():
    bets = read_json('./tmp/kingbets.json')
    write_log(f'[LIVESCORE]')
    datas = []
    for bet in bets:
        match_target = f"{bet['tournament']}-{bet['home_team']}-{bet['away_team']}"
        url, target_best, score = get_stage(match_target)
        if score > 0.3:
            data = get_score(url)
            datas.append(data)
            write_log(f'\t+ {match_target} > {target_best}: {score}')
    write_json(datas, './tmp/livescore.json')

if __name__ == '__main__':
    fetch_livescore_data()