#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import requests
import time
import datetime
import urllib2


# 创建一个类
class Port:
    ' 类的帮助信息'

    # 类变量
    def __init__(self, traceId, duration):
        self.traceId = traceId
        self.duration = duration


class Text:
    '创建类'

    def __init__(self, id, duration, parentId):
        self.id = id
        if parentId != None:
            self.parentId = parentId
        if duration != None:
            self.duration = duration


def date_to_str(date):
    return str(date)[0:10]


def before_days(num):
    today = datetime.date.today()
    oneday = datetime.timedelta(days=1)
    li = []
    for i in range(0, num):
        # 今天减一天，一天一天减
        today = today - oneday
        # 把日期转换成字符串
        li.append(date_to_str(today))
    return today


def get_time(times):
    timearray = time.strptime(times, "%Y-%m-%d %H:%M:%S")
    timestamp = int(time.mktime(timearray))
    return int(round(timestamp * 1000))


def get_duration(inter):
    return inter.duration


def display_duration(duration):
    tail = duration[-6:-3]
    top = duration[:-6]
    if int(duration[-3:-2]) > 5:
        tail = int(tail)
        tail = tail + 1
        if int(duration[-6:-5]) == 0:
            tail = '0' + str(tail)

    return top + '.' + str(tail) + ' s'


# 循环
def get_projects():
    projectDict = {}
    # 最低运行时间（微秒单位）
    # 科普:1秒=1000毫秒=1000000微秒
    minDuration = 1000000
    limit = 100000
    projectList = ['galaxy', 'evans', 'farmer', 'dna',  'careservice', 'civilization', 'cms',
                   'curvaturedrive', 'shooter', 'difoil','hdfragments']

                    #,'bye', 'dimension', 'era', 'singer','yolar', 'sophon','hibernation', 'huformation', 'kfb', 'mentalseal', 'midas', 'momentum', 'nsk', 'oldyolar',
                   #'owl', 'painter', 'redcoast', 'gateway', 'soalr', 'sophon', 'scientificboundary', 'dagon', ]

    startDate = date_to_str(before_days(7))
    buildStartTime = startDate + ' 00:00:00'
    startTime = get_time(buildStartTime)

    endTime = int(round(time.time()) * 1000)

    lockBack = endTime - startTime

    for project in projectList:
        values = {'serviceName': project, 'spanName': 'all', 'endTs': endTime,
                  minDuration: minDuration, 'limit': limit, 'lookback': lockBack, 'annotationQuery': '',
                  }

        r = requests.get("url", params=values)

        if r.status_code == requests.codes.ok:
            text = r.content

            d_text = json.loads(text)
            dicts = {}
            if len(d_text) != 0:
                portList = []
                # 把每个id拿出来 ，组装成list
                for key in d_text:
                    # 把每个接口组装成key_value形式 key:traceId ,value :key，key是个list
                    dicts[key[0]["traceId"]] = key

            # 把list中的key=id value=object
            for i in dicts:
                traceDicts = {}
                # 将list打开获取object
                for t in dicts[i]:
                    traceDicts[t['id']] = t

                for trace in dicts[i]:
                    addDuration = 0
                    if not hasattr(trace, 'parentId') or traceDicts.get(trace['duraparentIdtion']) == None:
                        if hasattr(trace, 'duration'):
                            addDuration = addDuration + int(trace['duration'])

                if addDuration == 0:

                    addDuration = dicts[i][0]['duration']
                    if len(str(addDuration)) > 6:
                        port = Port(trace["traceId"], addDuration)
                        portList.append(port)

            list = sorted(portList, key=get_duration, reverse=True)

            projectDict[project] = list

    return projectDict




def display_duration(duration):
    tail = duration[-6:-5]
    top = duration[:-6]
    if int(duration[-5:-4]) > 5:
        tail = int(tail)
        tail = tail + 1

    return str(top + '.' + str(tail) + ' s')


def project_owner():
    projectOwner = {}

    # key:project ,value:name
    # 小明
    list1 = ['galaxy', 'farmer', 'dna', 'sophon', 'difoil']
   
    for pro1 in list1:
        projectOwner[pro1] = ['小明', '11111111111']
    

    return projectOwner


def dingding(content, mobiles):
    url = "webhook"
    header = {
        "Content-Type": "application/json",
        "charset": "utf-8"
    }
    data = {
        "msgtype": "text",
        "text": {
            "content": "大家早上好:\n今日播报：耗时超过一秒的请求接口如下：\n" + content
        },
        "at": {
            "atMobiles": mobiles,
            "isAtAll": False
        }
    }

    sendData = json.dumps(data)
    request = urllib2.Request(url, data=sendData, headers=header)
    urlopen = urllib2.urlopen(request)
    print urlopen.read()


def main():
    content =get_projects()
    dingding(display_content(content), get_mobiles(content))


def display_content(content):
    display = '\n'
    # 创建一个保存项目的list
    for key in content:
        if len(content[key]) == 0:
            continue
        display = display + str(key) + ': @' + str(project_owner().get(key)[0]) + '\n'
        for port in content[key]:
            display = display + 'url' + str(
                port.traceId) + '\n' + 'duration:' + display_duration(
                str(port.duration)).rjust(10) + '\n'
            display = '%+10s' % display

        display = display + '\n'

    return display


def get_mobiles(content):
    # 组装电话号码
    top_three_mobile=[]
    mobiles = []
    for key in content:
        if len(content[key]) != 0:
            mobiles.append(project_owner().get(key)[1])

    from collections import Counter
    word_counts = Counter(mobiles)
    # 出现频率最高的3个单词
    top_three = word_counts.most_common(3)

    for mobile in top_three:
        top_three_mobile.append(mobile[0])

    return top_three_mobile


main()

