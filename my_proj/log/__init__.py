##################################################
# author: Lion.yu
##################################################

import os
import time
import calendar

ts = calendar.timegm(time.gmtime())

file_path = os.path.abspath(os.path.dirname(__file__))
logs_path = os.path.join(file_path, 'Logs')
errorlogs_path = os.path.join(file_path, 'ErrorLogs')

td = time.strftime('%Y-%m-%d',time.localtime(time.time()))
file_name = f'{td}_{ts}.txt'

logs_file = os.path.join(logs_path, file_name)
errorlogs_file = os.path.join(errorlogs_path, file_name)