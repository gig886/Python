# _*_ coding:utf-8 _*_

from bs4 import BeautifulSoup
import requests
from collections import deque
import os
import logging
import re
import threading

thread_lock = threading.RLock()

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='myapp.log',
                    filemode='w'
                    )

# 判断目录是否存在
def IsExistDir():
    for x in os.listdir('.'):
        if os.path.isdir(x) and x == 'picDir':
            return True
    return False


# 判断是否为需要的网址
def isfilter(strpage = str()):
    if len(strpage) == 0:
        return True
    filter1 = re.compile('com')
    filter2 = re.compile('cn')
    filter3 = re.compile('javascript')
    filter4 = re.compile('http')
    if len(filter1.findall(strpage)) > 0 or len(filter2.findall(strpage)) > 0 or len(filter3.findall(strpage)) or len(
            filter4.findall(strpage)):
        return True
    return False


# 页面解析
def parser(viewing_set, viewed_set, src_pic_set):
    while g_view_queue:
        current_url = g_view_queue.popleft()
        try:
            result_current = hu_session.get(current_url)
        except:
            logging.info("这个网址访问异常=================>" + current_url)
            continue
        try:
            result_current.encoding = 'utf-8'
            current_soup = BeautifulSoup(result_current.text, 'html.parser')
        except:
            logging.info("这个网址构建soup失败=================>" + current_url)
            continue
        body = current_soup.find('body')
        if body == None:
            logging.info("这个页面没有body=================>" + current_url)
            continue
        a_list = body.findAll('a', attrs={'href': True, 'target': False})
        img_list = body.findAll('img', attrs={'src': True})
        for a in a_list:
            attri = a['href']
            if isfilter(attri):
                continue
            url_list = attri.split('/')
            real_url = str()
            for i in range(len(url_list)):
                if len(url_list[i]) == 0:
                    continue
                real_url = real_url + '/' + url_list[i]
            print("原始地址：", attri)
            print("过滤后的地址：", real_url)
            view_url = r"http://10.78.13.168" + real_url
            if current_url == view_url:  # 如果解析出来的地址正好是正在访问的地址则跳过
                continue
            thread_lock.acquire()
            if view_url not in viewed_set and view_url not in viewing_set:
                viewing_set |= {view_url}
                thread_lock.release()
                g_view_queue.append(view_url)
        thread_lock.acquire()
        for img in img_list:
            src_pic_set |= {r"http://10.78.13.168/" + img['src']}
        thread_lock.release()
        thread_lock.acquire()
        viewed_set |= {current_url}
        thread_lock.release()

logging.info("开始爬行！")
g_view_queue = deque()  # 正在访问的页面队列
g_viewed = set()  # 已经访问过的页面
g_viewing = set()   # 将要访问的页面
g_src_pic = set()   # 图片地址
picDir = os.path.abspath('.')
if IsExistDir():
     picDir =  os.path.join(picDir,'picDir')
else:
    picDir = os.path.join(picDir, 'picDir')
    os.mkdir(picDir)  # 创建保存图片的目录

hu_session = requests.session()
start_url = 'http://10.78.13.168/InformationPlatform/'
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0'
}
dataInfo = {
    'username': 'gwhu',
    'password': '#0tdCxYdZwXyis1$'
}
result_login = hu_session.post('http://10.78.13.168/InformationPlatform/home/login',dataInfo,header)
g_viewing |= {start_url}
g_view_queue.append(start_url)
for i in range(10):
    create_thread = threading.Thread(target=parser, args=(g_viewing, g_viewed, g_src_pic))
    create_thread.start()
    create_thread.join()
logging.info("页面分析完毕，一共有%d个页面.", len(g_viewing))
picNo = int(0)
while len(g_src_pic) > 0:
    pic_url = g_src_pic.pop()
    try:
        result_pic = hu_session.get(pic_url)
    except:
        logging.info("这张图片访问异常============>"+pic_url)
        continue
    picNo += 1
    if result_pic.status_code == 200:
        filepath = os.path.join(picDir, str(picNo)+'.jpg')
        picfile = open(filepath, 'wb')
        picfile.write(result_pic.content)
        picfile.close()


logging.info("结束爬行！")




