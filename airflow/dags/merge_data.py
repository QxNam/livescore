import json

def merge():
    with open('/opt/airflow/dags/tmp/kingbets.json', 'r', encoding='utf-8') as f:
        bets = json.load(f)
    with open('/opt/airflow/dags/tmp/livescore.json', 'r', encoding='utf-8') as f:
        livescores = json.load(f)
    datas = []
    for bet, livescore in zip(bets, livescores):
        bet['period'] = livescore['period']
        # if bet['period']==1:
        #     bet['firsthalf_score'] = livescore['firsthalf_score']
        # else:
        bet['firsthalf_score'] = livescore['firsthalf_score']
        bet['fulltime_score'] = livescore['fulltime_score']
        datas.append(bet)
    with open('/opt/airflow/dags/tmp/merge_data.json', 'w', encoding='utf-8') as f:
        json.dump(datas, f, ensure_ascii=False, indent=4)
        
if __name__ == "__main__":
    merge()