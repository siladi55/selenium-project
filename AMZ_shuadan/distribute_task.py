# coding=utf-8
from work_process import Work
from work_process import *
from db.SQLModel import HandleDB
from logs.log import Logger
Log = Logger(__file__)
DB = HandleDB()
work = Work()

def main(interval=5):
    i = 0
    while 1:
        i += 1
        print '---ii---  ', i
        res = DB.callProc("exec sys_SelectTaskInfo")
        # print res
        if len(res[0]) > 1:
            if res[0][2] == 1:  # 注册
                task_guid = res[0][1]
                print 'reg1', task_guid
                work.regist_ini_account(task_guid)
            elif res[0][2] == 2:  # 流量刷单任务
                task_guid = str(res[0][1])
                print 'tas2', task_guid
                work.traffic_task(task_guid)
        time.sleep(interval)

if __name__ == '__main__':
    main()
