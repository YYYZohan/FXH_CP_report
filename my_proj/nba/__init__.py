##################################################
# author: Lion.yu
##################################################
import os
import toml
import pandas as pd
from my_proj.nba.base import Base_res

type_value = os.path.abspath(os.path.dirname(__file__)).split('/')[-1]
_conf_path = os.path.abspath(os.path.dirname(__file__))
conf_path = os.path.join(_conf_path, 'conf/conf.toml')

conf = toml.load(conf_path)

# 贝泰数据读取
BT_path = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
BT_file_path = os.path.join(BT_path, 'data/nba_players_info.csv')
BT_basic = pd.read_csv(BT_file_path)

# 基础方法初始化
Br = Base_res(conf_name='teamPlayerList', type=type_value)

# 篮球球队球员数据初始化
Gpi = Br.get_players_info()

# nba各榜单
rankType_dict = {
                "得分榜" : "basic.ptsAvg",
                "篮板榜" : "basic.rebAvg",
                "前场篮板榜" : "basic.orebAvg",
                "后场篮板榜" : "basic.drebAvg",
                "助攻榜" : "basic.astAvg",
                "抢断榜" : "basic.stlAvg",
                "盖帽榜" : "basic.blkAvg",
                "投篮命中率榜" : "basic.fgp",
                "三分总命中数榜" : "basic.tpm",
                "场均三分命中榜" : "basic.tpmAvg",
                "三分命中榜" : "basic.tpp",
                "罚球命中总数榜" : "basic.ftm",
                "场均罚球出手榜" : "basic.ftaAvg",
                "场均罚球命中榜" : "basic.ftmAvg",
                "罚球命中率榜" : "basic.ftp",
                "失误榜" : "basic.toAvg",
                "利用失误得分榜" : "basic.ptsOffTovAvg",
                "内线得分榜" : "basic.ptsInPaintsAvg",
                "内线命中率榜" : "basic.fgpInPaints",
                "二次进攻得分榜" : "basic.ptsSecondChanceAvg",
                "二次进攻命中率榜" : "basic.fgpSecondChance",
                "快攻得分榜" : "basic.ptsFastBreakAvg",
                "快攻命中率榜" : "basic.fgpFastBreak",
                "两双榜" : "basic.dd",
                "三双榜" : "basic.td",
                "犯规榜" : "basic.pfAvg",
                "犯满离场榜" : "basic.foulout",
                "技术犯规榜" : "basic.tf",
                "恶意犯规榜" : "basic.ff",
                "驱逐出场榜" : "basic.ejections",
                "上场时间榜" : "basic.minAvg",
                "+/-榜" : "basic.plusMinusAvg"
                }
