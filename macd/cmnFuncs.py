import math


def get_candle_price(item=None, tp=int()):
    """
        :param item:
            蜡烛图的基本值
            [时间，开，高，低，收，交易量]
        :param tp:
            0：开盘价
            1：最大值
            2：最小值
            3：收盘价
            4：平均值
        :return:
            根据tp类型，返回一个价格，float
            （时间戳，price)
    """
    if item is None:
        item = []
    if item.__len__() != 6:
        print(" 参数出错")
        return None

    tm = item[0]

    if tp < 4:
        price = float(item[tp + 1])
    else:
        price = (float(item[2]) + float(item[3])) / 2.0

    return tm, price


def compute_sd(item=None):
    """
        计算 标准差 (standard deviation)

    :param item:
        一系列数据

    :return:
        返回方差
    """

    if item is None:
        item = []
    if item.__len__() == 0:
        print(" 参数出错")
        return None

    sum = 0
    for val in item:
        sum += val

    ave = sum / float(item.__len__())

    var1 = 0

    for val in item:
        var1 += (val - ave) * (val - ave)

    return math.sqrt(var1 / float(item.__len__()))


def save_txt(file_name, data):
    with open(file_name, 'w', encoding='utf-8')as f:
        f.write(f'{data}\n')


def save_txt_append(file_name, data):
    with open(file_name, 'a+', encoding='utf-8')as f:
        f.write(f'{data}\n')

def read_file_txt(file_name):
    with open(file_name, 'r', encoding='utf-8')as f:
        data = f.read()
    return data

def compare_list(l1, l2):
    if l1 is None:
        l1 = []
    if l2 is None:
        l2 = []

    if l1.__len__() != l2.__len__():
        return False

    # for i in range(l1.__len__()):
    #     if l1[i] != l2[i]:
    #         return False

    # 仅仅比较两端相同
    if l1[0] == l2[0] and l1[-1] == l2[-1]:
        return True
    else:
        return False
