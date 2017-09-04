#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import urllib
from bs4 import BeautifulSoup

# 对网页进行访问，python中使用的是urllib库
resp = urllib.urlopen('http://admin.youhujia.com/nurse/login')

# 用于存放网页的html代码
html_data = resp.read().decode('utf-8')

soup = BeautifulSoup(html_data, "html.parser")
# 获取所有 <div id="nowplaying">格式的数据

print soup
nowplaying_movie = soup.find_all('div', id='nowplaying')

# 获取第一个
nowplaying_movie_list = nowplaying_movie[0].find_all('li', class_='list-item')

nowplaying_list = []
for item in nowplaying_movie_list:
    nowplaying_dict = {}
    nowplaying_dict['id'] = item['data-subject']
    for tag_img_item in item.find_all('img'):
        nowplaying_dict['name'] = tag_img_item['alt']
        nowplaying_list.append(nowplaying_dict)

print(nowplaying_list)

#找到评论链接https://movie.douban.com/subject/11502973/comments?start=0&limit=20

requrl = 'https://movie.douban.com/subject/'+nowplaying_list[0]['id']+'/comments?start=0&limit=20'
resp=urllib.urlopen(requrl)
html_data=resp.read().decode('utf-8')
soup=BeautifulSoup(html_data, "html.parser")
comment_div_lits=soup.find_all('div', class_='comment')

eachCommentList=[]
for item in comment_div_lits:
    if item.find_all('p')[0].string is not None:
       eachCommentList.append(item.find_all('p')[0].string)

# 清洗数据,将数据放在一个字符串中
#comments = ''
#for k in range(len(eachCommentList)):
#comments = comments+(eachCommentList[k]).strip()

#print(comments)

# 清除标点符号,利用正则表达式
#import re

#pattern = re.compile(r'[\u4e00-\u9fa5]+')
#filterdata = re.findall(pattern, comments)
#cleaned_comments = ''.join(filterdata)

#print(cleaned_comments)

#import jieba    #分词包
#import pandas as pd

#segment = jieba.lcut(cleaned_comments)
#words_df=pd.DataFrame({'segment':segment})