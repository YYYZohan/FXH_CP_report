from decimal import Decimal

def round_plus(data, index):
    if isinstance(index, int):
        _index = "{:." + str(index) +"f}"
        return _index.format(Decimal(data))
    else:
        print(f'index参数 必须为int类型 {index}')

print(round_plus(1.55, 1.1))