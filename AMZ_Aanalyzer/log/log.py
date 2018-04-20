#coding=utf-8
import logging


class Logger:
    def __init__(self, logName, logroot='flask.log', clevel=logging.DEBUG, Flevel=logging.INFO):
        self.logger = logging.getLogger(logName)
        self.logger.setLevel(logging.DEBUG)
        fmt = logging.Formatter('[%(asctime)s][%(levelname)7s][%(threadName)10s][%(process)d][%(name)15s]>> %(message)s',
                                '%Y-%m-%d %H:%M:%S')
        # 设置CMD日志
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        sh.setLevel(clevel)
        # 设置文件日志
        fh = logging.FileHandler(logroot)
        fh.setFormatter(fmt)
        fh.setLevel(Flevel)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def warn(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def critical(self, message):
        self.logger.critical(message)

    def exc(self, message):
        self.logger.exception(message)



if __name__ == '__main__':
   obj = Logger('AMZlog.log')
   obj.info('hahah')
   obj.debug('nvnvnv')
   obj.warn('waring!!')
'''
logger = logging.getLogger("AMZLogger")
logger.setLevel(logging.DEBUG)
# 建立一个filehandler来把日志记录在文件里，级别为debug以上
fh = logging.FileHandler("spam.log")
fh.setLevel(logging.DEBUG)
# 建立一个streamhandler来把日志打在CMD窗口上，级别为error以上
ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)
# 设置日志格式
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)
#将相应的handler添加在logger对象中
logger.addHandler(ch)
logger.addHandler(fh)
# 开始打日志
logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")
'''
