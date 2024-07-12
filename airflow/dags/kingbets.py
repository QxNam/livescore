import requests
import json, os

url = 'http://api.kingbets360.com:5002/api/v1/match-result'

def fetch_kingbets_data():
    try:
        response = requests.get(url)
        datas = response.json()
        not_esport = [data for data in datas if data['tournament'][:2]!='e-']
        if not_esport == []:
            response = requests.delete('http://livebbsw.ddns.net:8098/api/delall')
            raise Exception('No data found')
            
        with open('/opt/airflow/dags/tmp/kingbets.json', 'w', encoding='utf-8') as f:
            json.dump(not_esport, f, ensure_ascii=False, indent=4)
    except:
        raise Exception('Failed to fetch kingbets data')

def test():
    data = [
        {
            "id": 9531,
            "sport": "SOCCER",
            "tournament": "UEFA EURO 2024 (in Germany)",
            "game_id": "6933014",
            "game": "England / Netherlands",
            "home_team": "England",
            "away_team": "Netherlands",
            "date_event": "2024-07-10T15:00:00.1000000",
            "status": 0,
            "period": 2,
            "firsthalf_score": {
                "home_team": 1,
                "away_team": 1
            },
            "fulltime_score": {
                "home_team": 1,
                "away_team": 1
            }
        },
    ]
    print(os.getcwd())
    with open('/opt/airflow/dags/tmp/kingbets.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if __name__ == '__main__':
    # data = fetch_kingbets_data()
    # pprint(data)
    # test()
    fetch_kingbets_data()