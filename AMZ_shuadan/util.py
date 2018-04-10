#coding=utf-8
import time
import random
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class CidTransfer(object):
    cid2host_map = {1:'www.amazon.com', 2:'www.amazon.co.uk', 3:'www.amazon.ca',
                    4:'www.amazon.co.jp', 5:'www.amazon.de', 6:'www.amazon.fr',
                    7:'www.amazon.es', 8:'www.amazon.it', 9:'www.amazon.com.au'}
    host2cid_map = {v: k for k, v in cid2host_map.items()}

    def __init__(self, con):
        self.con = con

    @property
    def value(self):
        if self.con in list('123456789'):
            self.con = int(self.con)
        if self.con in CidTransfer.host2cid_map:
            return CidTransfer.host2cid_map[self.con]
        elif self.con in CidTransfer.cid2host_map:
            return CidTransfer.cid2host_map[self.con]
        else:
            raise ValueError('Wrong param! it should be like www.amazon.** or [1-9]')


def rand_stay(a=2, b=3):
    time.sleep(random.uniform(a, b))


def stay(r=992):
    rate = random.random() * 1000
    if rate > r:
        rand_stay(1, 4)

if __name__ == '__main__':
    print CidTransfer(9).value