#coding=utf-8
from excu.taskCtrler import *
from flask import Flask, request, render_template
from log.log import Logger
import os
app = Flask(__name__)
L = Logger('api')

@app.route('/')
def hello():
    # return render_template('info.html', name=name)
    return 'Hello haha'

@app.route('/1')
def res():
    return render_template('info.html')
    #return "4"

@app.route('/2')
def tes():
    res = test()
    return res

@app.route('/addTime')
def aTime():
    try:
        s = request.args['s']
        aList = s.split('<')
        res = addTime_ctrler(asinMD5List=aList)
        return res
    except:
        return -1

@app.route('/kwfromGA')
def GAkeyword():
    try:
        kw= request.args['kw']
        cid = int(request.args['cid'])
        res = adwords(kw, cid)
        return res
    except Exception, e:
        L.exc(e)

if __name__ == '__main__':
    # app.debug = True
    # handler = logging.FileHandler('flask.log')
    # handler.setLevel(logging.DEBUG)
    # logging_format = logging.Formatter(
    #     '[%(asctime)s][%(name)s][%(levelname)s][%(threadName)s]-line %(lineno)d>> %(message)s',
    #     '%Y-%m-%d %H:%M:%S')
    # handler.setFormatter(logging_format)
    # app.logger.addHandler(handler)
    app.run(host='0.0.0.0', port=5000)
