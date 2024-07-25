import requests
from utils import write_json, write_log

url = 'http://api.kingbets360.com:5002/api/v1/match-result'

def fetch_kingbets_data():
    response = requests.get(url)
    datas = response.json()
    not_esport = [data for data in datas if data['tournament'][:2]!='e-']
    if not_esport == []:
        response = requests.delete('http://livebbsw.ddns.net:8098/api/delall')
        raise Exception('No data found')
    
    write_json(not_esport, './tmp/kingbets.json')
    write_log(f'[KINGBETS] - {len(not_esport)} match')

def test():
    data = [
        {
            "id": 10878,
            "sport": "SOCCER",
            "tournament": "USA Major League Soccer",
            "game_id": "6963184",
            "game": "Los Angeles FC / Columbus Crew",
            "home_team": "Los Angeles FC",
            "away_team": "Columbus Crew",
            "date_event": "2024-07-13T22:30:00.1000000",
            "status": 0,
            "period": 2,
            "firsthalf_score": {
            "home_team": 0,
            "away_team": 1
            },
            "fulltime_score": {
            "home_team": 1,
            "away_team": 5
            }
        },
        {
            "id": 10879,
            "sport": "SOCCER",
            "tournament": "USA Major League Soccer",
            "game_id": "6963186",
            "game": "San Jose Earthquakes / Sporting Kansas City",
            "home_team": "San Jose Earthquakes",
            "away_team": "Sporting Kansas City",
            "date_event": "2024-07-13T22:30:00.1000000",
            "status": 0,
            "period": 2,
            "firsthalf_score": {
            "home_team": 0,
            "away_team": 0
            },
            "fulltime_score": {
            "home_team": 1,
            "away_team": 2
            }
        }
    ]

    write_json(data, './tmp/kingbets.json')
    write_log(f'[KINGBETS] - {len(data)} match')

if __name__ == '__main__':
    fetch_kingbets_data()
    # test()
