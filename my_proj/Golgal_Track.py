##################################################
# author: Lion.yu
##################################################
from decimal import Decimal
import hashlib

def sort_df(df, columns):
    if isinstance(columns, str) or isinstance(columns, list):
        df.sort_values(by=columns, ascending=False, inplace=True)
        return df
    else:
        print(f'参数{columns} 类型错误')
        return


# 优化四舍五入 代替 round
def round_plus(data, index):
    if isinstance(index, int) and index >= 0:
        _index = "{:." + str(index) +"f}"
        return _index.format(Decimal(data))
    else:
        print(f'index参数 必须为int类型 {index}')
        return 


def url_link(con):
    pass

def md5(data):
    return hashlib.md5(bytes(data,encoding='utf8')).hexdigest()