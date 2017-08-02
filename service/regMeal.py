# 登录信息平台，加班签到
import requests
import time
import datetime

global logger_
def getLogger():
    import inspect
    import logging
    import os
    logger = logging.getLogger('[RegMeal]')
    this_file = inspect.getfile(inspect.currentframe())
    dirpath = os.path.abspath(os.path.dirname(this_file))
    handler = logging.FileHandler(os.path.join(dirpath, 'regMeal.log'))
    formatter = logging.Formatter('%(asctime)s  %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
    return logger

logger_ = getLogger()

def regMeal(username='',password=''):
    loginUrl = 'http://10.78.13.168/InformationPlatform/home/login'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
    }
    dataInfo = {
        'username': username,
        'password': password
    }
    hu_session = requests.session()
    # 登录
    result_login = hu_session.post(loginUrl, dataInfo, header)
    # 签到
    regUrl = 'http://10.78.13.168/InformationPlatform/meal/register/'
    result_reg = hu_session.post(regUrl)
    logger_.info(result_reg.text)

def convertTimeStampToStrTime(timestamp):
    timeArray = time.localtime(timestamp)
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    return strTime


def convertStrTimeToTimeStamp(strTime):
    timeArray = time.strptime(strTime, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(timeArray))
    return timestamp


def IsReg(timestamp): #是否是签到的时间点
    currentDate = str(datetime.date.today())
    currentDataStart = currentDate + ' 18:40:00'
    currentTimeStampStart = convertStrTimeToTimeStamp(currentDataStart)

    currenDataEnd = currentDate + ' 20:00:00'

    currentTimeStampEnd = convertStrTimeToTimeStamp(currenDataEnd)
    if currentTimeStampStart <= timestamp <= currentTimeStampEnd:
        return True
    else:
        return False

def IsRegDate(s3 = ''): #判断是不是签到的日期
    dayOfWeek = datetime.date.today().weekday()
    if str(dayOfWeek) in s3:
        return True
    else:
        return False

def printTime(): #打印时间
    timestamp = int(time.time())
    logger_.info('当前时间为：', convertTimeStampToStrTime(timestamp))

def main(s1 = '', s2 = '', s3 = ''):
    try:
        logger_.info('程序启动！')
        i = 0
        while(True):
            printTime()
            while(True):
                timestamp = int(time.time())
                if IsReg(timestamp) and IsRegDate(s3):
                    regMeal(s1, s2)
                    printTime()
                    i = i + 1
                    logger_.info("签到成功！")
                    time.sleep(86400)
                    break
                else:
                    logger_.info("不是签到时间，一个小时之后再试！")
                    time.sleep(3600)
            if 4 == i:
                break
    except:
        logger_.info('程序异常退出！')
        return False
    else:
        logger_.info('程序正常退出！')
        return False
