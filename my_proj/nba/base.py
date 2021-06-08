##################################################
# author: Lion.yu
##################################################

import os
import requests
import json
import time
import toml
import numpy as np
import pandas as pd


bisic_data_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
bisic_data_path = os.path.join(bisic_data_path, 'data/nba_players_info.csv')
bisic_data = pd.read_csv(bisic_data_path)

conf_path = os.path.abspath(os.path.dirname(__file__))
conf_path = os.path.join(conf_path, 'conf/conf.toml')


# 动态生成比赛类型参数
def competitionType(data,type):
    data['competitionLeagueType'] = data['competitionType'] = type
    return data

# 基础数据请求
class Base_res():
    def __init__(self, conf_name, type):
        print("基础数据初始化...")
        # 读取配置
        self.conf = toml.load(conf_path)
        self.t1 = time.time()
        self.conf_name = self.conf[conf_name]
        self.type = type

    # 获取球队id
    def get_teamids(self):
        api_info = self.conf['teamStandingList']
        url = api_info['url']
        _data = json.loads(api_info['data'])
        data = competitionType(_data, self.type)
        header = json.loads(api_info['header'])
        req = requests.get(url=url,headers=header,params=data)
        if req.status_code == 200 and req.json()['errorCode'] == "":
            res = req.json()['result']['rankTypeListMap']
            # 东部排行球队
            res_E = res["E"]
            res_E_teamids = [{i['teamName'] : i['teamId']} for i in res_E]
            # 西部排行球队
            res_W = res["W"]
            res_W_teamids = [{i['teamName'] : i['teamId']} for i in res_W]
            all_teamids = res_E_teamids + res_W_teamids
            final_res = {}
            for i in all_teamids:
                for key, value in i.items():
                    final_res[key] = value
            return final_res
        else:
            return "teamStandingList 接口请求失败"

    # 获取球员数据 
    def get_player_info(self,teamId):
        api_info = self.conf_name
        url = api_info['url']
        _data = json.loads(api_info['data'])
        header = json.loads(api_info['header'])
        _data['teamId'] = teamId
        data = competitionType(_data, self.type)
        
        req = requests.get(url=url,headers=header,params=data)
        if req.status_code == 200 or req.json()['errorCode'] == "":
            team_name = req.json()['result']['info']['name']
            _result = req.json()['result']['list']
            result = []
            for i in _result:
                i['team_name'] = team_name
                result.append(i)
            return pd.DataFrame(result).drop(columns=["player_header", "player_header_big", "salary", "salary_str"])
        else:
            print(req.json())
            return "teamStandingList 接口请求失败"

    # 获取所有球队的球员信息
    def get_players_info(self):
        result = pd.DataFrame()
        print("Start loading Players info...")
        for i, j in self.get_teamids().items():
            result = pd.concat([result, self.get_player_info(j)],axis=0)
        t2 = time.time()
        print(f"All Players info was loaded, used up {round(t2-self.t1, 2)} sec")
        pop = result.pop('team_name')
        result.insert(0, 'team_name', pop)
        result['playerName'] = result['player_name']
        result['ast'] = result['asts']
        result.replace('', 0, inplace=True)
        result.fillna(0, inplace=True)
        return result

def sort_df(df, columns):
    if isinstance(columns, str) or isinstance(columns, list):
        df.sort_values(by=columns, ascending=False, inplace=True)
        return df
    else:
        print(f'参数{columns} 类型错误')
        return
