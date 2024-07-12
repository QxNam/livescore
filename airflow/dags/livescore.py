import requests, json
from datetime import datetime
from dotenv import dotenv_values
from cosine import the_nearest

# --- init base ---
url = 'https://www.livescore.com/_next/data/LbC2S31VjzszcKPHb0uaY/en/football/{cmnt}/{scd}/{t1}-vs-{t2}/{eid}.json'
url_live = 'https://prod-public-api.livescore.com/v1/api/app/live/soccer/7?locale=en&MD=1'
# url_live = 'https://prod-public-api.livescore.com/v1/api/app/stage/soccer/euro-2024/semi-finals/7?locale=en&MD=1'
date = datetime.now().strftime('%Y%m%d')
configs = dotenv_values('.env')
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
            datas[f'{cnm}-{t1}-{t2}'] = url.format(cmnt=cmnt, scd=scd, t1=t1, t2=t2, eid=eid)
    value, target_best, score = the_nearest(datas, match_target)
    return value

def get_score(url='https://www.livescore.com/_next/data/LbC2S31VjzszcKPHb0uaY/en/football/euro-2024/semi-finals/spain-vs-france/1274137.json'):
    data = {}
    response = requests.get(url)
    data_json = response.json()['pageProps']['initialEventData']['event']
    for key, value in DATA.items():
        data[key] = _collect_data(data_json, value)
    data['period'] = len(data['period'].keys())
    print(data['period'])
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

def crawl():
    with open('/opt/airflow/dags/tmp/kingbets.json', 'r', encoding='utf-8') as f:
        bets = json.load(f)
    datas = []
    for bet in bets:
        match_target = f"{bet['tournament']}-{bet['home_team']}-{bet['away_team']}"
        url = get_stage(match_target)
        data = get_score(url)
        datas.append(data)
    with open('/opt/airflow/dags/tmp/livescore.json', 'w', encoding='utf-8') as f:
        json.dump(datas, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    crawl()