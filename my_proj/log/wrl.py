##################################################
# author: Lion.yu
##################################################
from my_proj.log import logs_file, errorlogs_file

def WRL(data, matches_value):
    if matches_value == 1:
        with open(logs_file, 'w+') as f:
            f.write(data)
    else:
        with open(logs_file, 'w+') as f:
            f.write(data)
        with open(errorlogs_file, 'w+') as ff:
            ff.write(data)

