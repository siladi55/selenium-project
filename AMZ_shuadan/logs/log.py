# encoding=utf-8
import logging
import logging.handlers
import os

# 日志文件的路径，FileHandler不能创建目录，这里先检查目录是否存在，不存在创建他
# 当然也可以继承之后重写FileHandler的构造函数
LOG_FILE_PATH = os.path.join(os.path.split(os.path.realpath(__file__))[0], "Execution.logs")
dir = os.path.dirname(LOG_FILE_PATH)
if not os.path.isdir(dir):
    os.mkdir(dir)
LOGNAME = ''  # root logs


class Logger(object):
    """logger的配置"""

    def __init__(self, logName, file_level='DEBUG', console_level='INFO', logFile=LOG_FILE_PATH):
        self.config(logName, logFile, file_level, console_level)

    def config(self, logName, logFile, file_level, console_level):
        # 生成root logger
        self.logger = logging.getLogger(logName)
        self.logger.setLevel(file_level)
        self.fh = logging.handlers.RotatingFileHandler(logFile, mode='a', maxBytes=1024 * 1024 * 10, backupCount=100,
                                                       encoding="utf-8")
        self.fh.setLevel(file_level)
        # 生成StreamHandler
        self.ch = logging.StreamHandler()
        self.ch.setLevel(console_level)
        # 设置格式
        formatter = logging.Formatter("[%(asctime)s]-[%(name)s]-[%(lineno)d]-[%(levelname)s]>> %(message)s")
        self.ch.setFormatter(formatter)
        self.fh.setFormatter(formatter)
        # 把所有的handler添加到root logger中
        self.logger.addHandler(self.ch)
        self.logger.addHandler(self.fh)

    def debug(self, msg):
        if msg is not None:
            self.logger.debug(msg)

    def info(self, msg):
        if msg is not None:
            self.logger.info(msg)

    def warning(self, msg):
        if msg is not None:
            self.logger.warning(msg)

    def error(self, msg):
        if msg is not None:
            self.logger.error(msg)

    def critical(self, msg):
        if msg is not None:
            self.logger.critical(msg)

    def exc(self, msg):
        if msg is not None:
            self.logger.exception(msg)



if __name__ == "__main__":
    LOG = Logger(LOGNAME)
    # 测试代码
    # for i in range(50):
    #     LOG.error(i)
    #     LOG.debug(i)
    LOG.critical("Database has gone away")
