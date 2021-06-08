##################################################
# author: Lion.yu
##################################################

import os
import pandas as pd
from my_proj.log import logs_path, errorlogs_path, file_name
from my_proj.log.wrl import WRL
from my_proj.notice import dd_notice
from my_proj.notice.dd_notice import send_message


def dfc(df1, df2):
    if df1.shape[0] != df2.shape[0]:
        print(f'{df1}数据行数: {df1.shape[0]},{df2}数据行数: {df2.shape[0]}')
        return False
    else:
        import datacompy
        compare = datacompy.Compare(df1, df2)
        if compare.matches():
            WRL(file_name=os.path.join(logs_path, file_name), data=compare.matches())
        else:
            send_message(compare.report())
            WRL(file_name=os.path.join(logs_path, file_name), data=compare.report())
            WRL(file_name=os.path.join(errorlogs_path, file_name), data=compare.report())
            return compare.report()
    