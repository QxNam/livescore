import requests, json
from pprint import pprint

def post():
    with open('/opt/airflow/dags/tmp/merge_data.json', 'r', encoding='utf-8') as f:
        datas = json.load(f)
    header = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYmJzdyIsImV4cCI6MTcyMDUyNTY5M30.kdhYZ3DibsU6fCkDg-Nh21of5Y5YtZ5802ttCvkzJ70'
    }
    response = requests.patch('http://livebbsw.ddns.net:8098/api/updateall', headers=header, json=datas)
    if response.status_code == 201:
        print('Success')
    else:
        print('Failed', response.status_code)
        
if __name__ == '__main__':
    post()