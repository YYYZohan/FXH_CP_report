##################################################
# author: Lion.yu
##################################################
import json
import requests
import time
import pandas as pd
from my_proj.nba import conf, type_value, Gpi, rankType_dict, BT_basic
from my_proj.nba.base import competitionType, sort_df
from my_proj.compare import dfc
from my_proj.Golgal_Track import md5, round_plus
from my_proj.notice.dd_notice import send_message
from my_proj.log.wrl import WRL
from my_proj.log import file_name


# 数据准备
pSDSR = conf['playerSingleDimensionSeasonRank']
url = pSDSR['url']
_data = json.loads(pSDSR['data'])
header = json.loads(pSDSR['header'])
data = competitionType(_data, type_value)

# 本地记录比对次数
matches_num = []

# 比对执行耗时-开始时间记录
compare_start_time = time.time()

# 球员赛季数据请求
for i, j in rankType_dict.items():
    data['rankType'] = j
    res = requests.get(url=url,headers=header,params=data)
    if res.status_code != 200 and res.json()["errorCode"] != "":
        print(f'参数可能有误 key-->{i},values-->{j}')
    res_df = pd.DataFrame(res.json()['result']['rankInfoList'])
    res_df = res_df[['playerId', 'playerName', 'teamId','value','pts', 'reb', 'ast', 'stl']]
    res_df['index'] = res_df['playerId'].astype('str') + res_df['teamId'].astype('str')
    res_df['index'] = res_df['index'].apply(md5)
    BT_basic_df = BT_basic[BT_basic['index'].isin(res_df['index'].to_list())]
    

    # 处理并统一BT_basic_df 表头
    BT_basic_df = BT_basic_df[['new_playerid' ,'lastname', 'new_teamid', 'average_points', 'average_rebounds', 'average_assists', 'average_steals', 'index']]
    BT_basic_df.rename(columns={
                                'new_playerid' : 'playerId',
                                'average_points' : '场均得分', # pts
                                'average_rebounds' : "场均篮板", # reb
                                'average_assists' : "场均助攻", # ast
                                'average_steals' : "场均抢断", # stl
                                'new_teamid' : 'teamId',
                                'lastname' : 'playerName'
                                },
                                inplace=True
                                )

    # 注意!!! 相关需比对的字段后续会被做为索引，故两个df索引类型必须保持一致，此处统一强转str
    BT_basic_df['playerId'] = BT_basic_df['playerId'].astype('str')
    BT_basic_df['teamId'] = BT_basic_df['teamId'].astype('str')

    # reb、stl 需保留1位小数
    BT_basic_df['场均篮板'] = BT_basic_df['场均篮板'].apply(round_plus, index=1)
    BT_basic_df['场均抢断'] = BT_basic_df['场均抢断'].apply(round_plus, index=1)                
    res_df.pop('value')
    # res_df.pop('playerName')

    res_df.rename(columns={
                            'pts' : '场均得分', # pts
                            'reb' : "场均篮板", # reb
                            'ast' : "场均助攻", # ast
                            'stl' : "场均抢断", # stl
                            'lastname' : 'playerName'
                            },
                            inplace=True
                            )
                            
    import datacompy
    Cp = datacompy.Compare(BT_basic_df, res_df, join_columns=['index', 'playerId', 'teamId', 'playerName'], df1_name='贝泰数据源', df2_name='篮球内部接口数据')

    # 比对结果写入日志
    if Cp.matches():
        WRL(data=Cp.report(),matches_value=1)
        matches_num.append(Cp.matches())
    else:
        WRL(data=Cp.report(),matches_value=2)
        matches_num.append(Cp.matches())

# # 比对结束时间记录
# compare_end_time = time.time()
# # 比对耗时
# compare_used_time = round_plus(compare_end_time - compare_start_time, 2)

# if len(set(matches_num)) == {True}:
#     send_message('Test\n球员赛季数据比对完成，PASS！',cp_resp=1)
# else:
#     wrong_num = []
#     for i in matches_num:
#         if i is not True:
#             wrong_num.append(i)
#     send_message(f'Test Compare is Finshed!\n NBA 球员赛季数据比对完成，FAIL！总共{len(wrong_num)} 处错误,请联系 @郁晟亮 发送错误记录\n 文件名:\n{file_name}\n',cp_resp=0)
