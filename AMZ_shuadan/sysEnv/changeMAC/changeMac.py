#coding=utf-8
import sys, os
reload(sys)
sys.setdefaultencoding('utf-8')
import time
import random
import subprocess
import re
import platform
from logs.log import Logger
L = Logger(__file__)


def modify_mac(mac):
    """修改sys的mac地址"""
    bat1 = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'reg_add.bat')
    bat2 = os.path.join(os.path.split(os.path.realpath(__file__))[0], 'reconnect.bat')
    try:
        cmd = "{0} {1}".format(bat1, mac)
        os.popen(cmd)
        time.sleep(0.2)
        os.popen(bat2)
    except:
        L.exc('网卡修改执行错误')


def random_mac(index):
    """index: 传入前6位mac字符，网卡厂商标识，随机生成新mac地址"""
    Maclist = [index.upper().replace(':', '-')]
    for i in range(1, 4):
        RANDSTR = "".join(random.sample("0123456789abcdef", 2)).upper()
        Maclist.append(RANDSTR)
    RANDMAC = "-".join(Maclist)
    print RANDMAC
    return RANDMAC

def connect_status(mac):
    """判断能否上网"""
    ret = os.system('ping 8.8.8.8')
    # if connected, ret will return 0, otherwise 1
    if not ret and (mac in find_all_mac()):
        L.info('网卡修改成功')
        return True
    else:
        L.info('网卡修改失败')
        return False

def find_all_mac():
    macList = []
    data = os.popen('ipconfig /all').readlines()
    for i in range(len(data)):
        data[i] = data[i].decode('GBK').encode('utf-8')
    i = 0
    for line in data:
        if "物理地址" in line:
            mac = line.split(":")[-1].strip()
            macList.append(mac)
    return macList


def set_mac(given_mac=None, index='00:03:DC'):
    """if mac is not specified, generate a random new mac.
        new mac starts with index
        The second letter has to be one of [0、2、4、6、8、A、C、E]
        if mac is given, modify the mac accordingly
    """
    assert index[1].lower() in ('0', '2', '4', '6', '8', 'a', 'c', 'e'), 'Wrong mac'
    mac = given_mac if given_mac else random_mac(index)
    modify_mac(mac)
    time.sleep(5)
    return mac, connect_status(mac)


if __name__ == '__main__':
    # set_mac(index='00:15:23')
    set_mac('00-20-AB-D2-95-DA')
    # find_all_mac()
