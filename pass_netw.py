# author: sylacd
# date : 2020.02.15

import pandas as pd
import numpy as np
from copy import copy

def getData(period='0H', time=0, match=0, team='Huskies', timelast=300):
    'This function is used to flitering the data by team, matchID, and so on. match=0 means return all matches. period=0H means return the total match, and time is not used at that time.'
    data = pd.read_csv("E:\\syl_in_SJTU\\mcm2\\2020_Problem_D_DATA\\passingevents.csv")
    data = data[data['TeamID'].isin([team])]
    if match is not 0:
        data = data[data['MatchID'].isin([match])]
    if period is not '0H':
        data = data[data['MatchPeriod'].isin([period])]
        if time > data.iloc[-1]['EventTime']:
            return None
        if (time + timelast) > data.iloc[-1]['EventTime']:
            data = data[data['EventTime'] >= time]
        else:
            data = data[(data['EventTime'] >= time) & (data['EventTime'] < (time + timelast))]
    data = data.reset_index(drop=True)
    return data

def getPlayers(csv_data):
    'Return the list of players playing in the ordered period.'
    name = dict.fromkeys(csv_data['OriginPlayerID'])
    name2 = dict.fromkeys(csv_data['DestinationPlayerID'])
    name.update(name2)
    return list(name.keys())

def getAdjMatrix(csv_data, player):
    'Return the adjacent matrix of the passing network.'
    adj = pd.DataFrame({}, index=player, columns=player)
    adj = adj.fillna(0)
    for i in range(csv_data.shape[0]):
        if csv_data.loc[i, 'OriginPlayerID'] != csv_data.loc[i, 'DestinationPlayerID']:
            adj.loc[csv_data.loc[i, 'OriginPlayerID'], csv_data.loc[i, 'DestinationPlayerID']] += 1
    print(adj)
    return adj
        

if __name__ == '__main__':
    data = getData(period='1H', time=0, match=1, timelast=2000)
    players = getPlayers(data)
    getAdjMatrix(data, players)