#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import poplib
import re
from email.parser import Parser
from logs.log import Logger
Log = Logger(__file__)


class MailServer(object):
    def __init__(self, user, pw, host, port=110):
        self.user = user
        self.pw = pw
        self.host = host
        self.port = port
        self.server = None
        self.conn = self.mail_recv()

    def mail_recv(self):
        """port: 110 standard port, 995 SSL port"""
        if self.port not in (110, 995):
            Log.error('POP port param should be in (110, 995)')
            return False
        self.server = poplib.POP3(self.host, self.port) if self.port == 110 \
            else poplib.POP3_SSL(self.host, self.port)
        try:
            self.server.user(self.user)
            self.server.pass_(self.pw)
            Log.info('<mail recv> Mail server connected!')
            return True
        except:
            Log.exc('<main server>:Wrong secret token or with no permession.')
            return False

    def email_counts(self):
        print('Emails Num: %s. Size: %s' % self.server.stat())
        # resp, mails, otces = self.server.list()
        # print 'mails:',mails
        # return len(mails)  # 最新的邮件index等于listings的长度
        return int(self.server.stat()[0])

    def parse_mail(self, index):
        # 解析最新(index：最新邮件下标)一封邮件
        resp, lines, octets = self.server.retr(index)
        msg_content = '\r\n'.join(lines)
        msg = Parser().parsestr(msg_content)
        # print msg, 'msg'
        part = msg.get_payload()[0]  # [0]默认为文本信息，而parts[1]默认为添加了HTML代码的数据信息
        if part.get_content_maintype() == 'text':
            return part.get_payload(decode=True).strip()
        else:
            print part.get_content_maintype(), '新的manitype'
            return part.get_payload().strip()

    def abstract_authcode(self, mail_content, pattern=r'>(\d{6})<'):
        res = re.findall(pattern, mail_content)
        return res[0] if len(res) else None

    def close_server(self):
        self.server.quit()

if __name__ == '__main__':
    obj = MailServer('arjun_deora@rurumail.com', '150587', 'pop.rurumail.com')
    print obj.abstract_authcode(obj.parse_mail(obj.email_counts()))
