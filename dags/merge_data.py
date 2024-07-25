from utils import *
from datetime import datetime
def merge():
    bets = read_json('./tmp/kingbets.json')
    livescores = read_json('./tmp/livescore.json')

    datas = []
    for bet, livescore in zip(bets, livescores):
        bet['period'] = livescore['period']
        # if bet['period']==1:
        #     bet['firsthalf_score'] = livescore['firsthalf_score']
        # else:
        bet['firsthalf_score'] = livescore['firsthalf_score']
        bet['fulltime_score'] = livescore['fulltime_score']
        datas.append(bet)
    write_json(datas, './tmp/merge_data.json')
    write_log(f'[MERGER ID]')
        
if __name__ == "__main__":
    merge()