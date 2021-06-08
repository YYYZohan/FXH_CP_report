##################################################
# author: Lion.yu
##################################################
import time
import requests
import json
import os
import toml
import pandas as pd
from my_proj.Golgal_Track import round_plus

conf_path = os.path.abspath(os.path.dirname(__file__))
conf_path = os.path.join(conf_path, 'beitai_conf.toml')

class BT_base():
    def __init__(self):
        self.a = time.time()
        print('BEITAI data is Initializing...\nWill be use 3-5 minutes...')
        self.conf_info = toml.load(conf_path)
        self.uri = self.conf_info['default_con']['uri']
        self.data = self.conf_info['default_con']['data']
        self.headers = self.conf_info['default_con']['header']

    # 球队列表接口
    def get_teams_info(self):
        api_info = self.conf_info['teamlist']
        url = self.uri + api_info['router']
        data = json.loads(self.data)
        header = json.loads(self.headers)
        res = requests.get(url=url, params=data, headers=header)
        if res.status_code == 200 and res.json()['btsstate']:
            res_df = pd.DataFrame(res.json()['teams'])
            res_df = res_df[['teamid', 'teambeitainame', 'teamname']]
            return res_df
        else:
            print(f'{url} 请求失败')
            return

    # 球员列表接口
    def get_players_info(self):        
        api_info = self.conf_info['playerlist']
        url = self.uri + api_info['router']
        data = json.loads(self.data)
        header = json.loads(self.headers)
        extra_df = pd.DataFrame()
        for i, j in self.get_teams_info().iterrows():
            data['teamid'] = j['teamid']
            try:
                res = requests.get(url=url, params=data, headers=header)
                if res.status_code == 200 and res.json()['btsstate']:
                    res_df = pd.DataFrame(res.json()['players'])
                    res_df = res_df[['lastname', 'fullname', 'playerid']]
                    res_df['teamid'] = data['teamid']
                    res_df['teambeitainame'] = j['teambeitainame']
                    res_df['teamname'] = j['teamname']
                    extra_df = pd.concat([extra_df, res_df], axis=0)
                    # time.sleep(2)
                else:
                    print(f'{url} 请求失败')
                    return
            except requests.exceptions.ConnectionError as CE:
                print(CE)
        extra_df.dropna(inplace=True)
        return extra_df

    # 自由球员列表接口
    def get_freeagents_info(self):
        api_info = self.conf_info['freeagents']
        url = self.uri + api_info['router']
        data = json.loads(self.data)
        res = requests.get(url=url, params=data)
        try:
            if res.status_code == 200 and res.json()['btsstate']:
                res_df = pd.DataFrame(res.json()['freeagents'])
                res_df = res_df[['lastname', 'fullname', 'playerid']]
                res_df['teamid'] = 0
                res_df['teambeitainame'] = res_df['teamname'] = '无'
                res_df.dropna(inplace=True)
                return res_df
            else:
                print(f'{url} 请求失败')
                return
        except requests.exceptions.ConnectionError as CE:
            print(CE)

    # 整合所有球员
    def concat_all_players(self):
        return pd.concat([self.get_players_info(), self.get_freeagents_info()], axis=0)


    # 指定球员赛季数据接口 (所有球员数据df)
    def getplayerstats(self, matchtype='REG'):
        api_info = self.conf_info['getplayerstats']
        url = self.uri + api_info['router']
        data = json.loads(self.data)
        data['matchtype'] = matchtype
        extra_df = pd.DataFrame()
        for i, j in self.concat_all_players().iterrows():
            data['playerid'] = j['playerid']
            try:
                res = requests.get(url=url, params=data)
                if res.status_code == 200 and res.json()['btsstate']:
                    res_df = pd.DataFrame(res.json()['playerStatsList'])
                    extra_df = pd.concat([extra_df, res_df], axis=0)
                else:
                    print(f'{url} 请求失败')
                    return 
            except requests.exceptions.ConnectionError as CE:
                print(CE)
        print(f"Loading is Compalted! Used {round_plus(time.time()-self.a,2)} sec!")
        # extra_df.to_csv('extra_df.csv')
        return extra_df
        
    # 本地映射虎扑对应id
    def id_mapping(self, id, idType):
        url = "http://msv-zuul-stg.hupu.io/basketball-ds-msv/source-id-mapping"
        data = {
                "outBizType" : idType,
                "outBizSource" : "BEITAI",
                "outBizNo" : id
                }
        try:
            res = requests.get(url=url,json=data)
            if res.json()['bizNo']:
                return res.json()['bizNo']
            else:
                print('bizNo 字段不存在')
                return 
        except requests.exceptions.ConnectionError as CE:
            print(CE)
            return 
    
    # 本地添加球队球员 id mapping
    def total_df(self):
        b = time.time()
        getplayerstats = self.getplayerstats()
        print('Start Processing data...')
        aa = time.time()
        getplayerstats['new_playerid'] = getplayerstats['playerid'].apply(self.id_mapping, idType='NBA_PLAYER')
        getplayerstats['new_teamid'] = getplayerstats['teamid'].apply(self.id_mapping, idType='NBA_TEAM')

        # 添加唯一索引(球员id 拼接 球队id)
        from my_proj.Golgal_Track import md5
        getplayerstats['index'] = getplayerstats['new_playerid'].astype('str') + getplayerstats['new_teamid'].astype('str')
        getplayerstats['index'] = getplayerstats['index'].apply(md5)

        # 数据导出 csv
        df_path = os.path.abspath(os.path.dirname(__file__))
        df_path = os.path.join(df_path, 'data')
        getplayerstats.to_csv(f'{df_path}/nba_players_info.csv')
        print(f"Processing is Compalted! Used {round_plus(time.time()-aa,2)} sec!")
        print(f"All Missions were Used {round_plus(time.time()-self.a,2)} sec!")


# 基础数据初始化调用
BTBS = BT_base()
BTBS.total_df()

