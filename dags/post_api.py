import requests
from utils import *

def post():
    datas = read_json('./tmp/merge_data.json')
    header = {
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYmJzdyIsImV4cCI6MTcyMDUyNTY5M30.kdhYZ3DibsU6fCkDg-Nh21of5Y5YtZ5802ttCvkzJ70'
    }
    response = requests.patch('http://livebbsw.ddns.net:8098/api/updateall', json=datas)
    write_log(f'[POST] - {response.status_code}')
    write_log('*'*120)
    # print(response.status_code)
        
if __name__ == '__main__':
    post()