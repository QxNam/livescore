import requests
from pprint import pprint
header = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjoiYmJzdyIsImV4cCI6MTcyMDUyNTY5M30.kdhYZ3DibsU6fCkDg-Nh21of5Y5YtZ5802ttCvkzJ70'
}

res = requests.get('http://171.247.106.138:8098/api', headers=header)
pprint(res.json())