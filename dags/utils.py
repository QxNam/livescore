import json
import pytz
from datetime import datetime
now = datetime.now(tz=pytz.timezone('Asia/Saigon')) #Ho_Chi_Minh

def write_json(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def write_log(text):
    with open(f'./logs/{now.date()}.txt', 'a+', encoding='utf-8') as f:
        f.write(f'{now.time()} - {text}\n')

def read_json(path='./tmp/kingbets.json'):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)