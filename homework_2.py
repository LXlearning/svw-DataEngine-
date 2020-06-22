import requests
from bs4 import BeautifulSoup
import pandas as pd


"""
    Action1：汽车投诉信息采集：
    数据源：http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-1.shtml
    投诉编号，投诉品牌，投诉车系，投诉车型，问题简述，典型问题，投诉时间，投诉状态
    可以采用Python爬虫，或者第三方可视化工具
"""


#此函数用于从url中获取html文档
def requesturl(url):
    r=requests.get(url)
    if r.status_code!=200:
        raise Exception()
    html_doc=r.text
    soup = BeautifulSoup(html_doc,features="lxml") # BeautifulSoup的解析器
    return soup

#此函数用于从html文档中解析得到需求的字符串，并写入到列表中
def parsesoup(soup):        
    str = soup.find("div",class_="tslb_b")
    tr_list = str.find_all('tr')[1:]#第0行为标题行，不需要它
    tablelist=[]
    for line in tr_list:
        tdlist=line.find_all('td')#在某行中，不同的列的值存在td标签下
        rowlist=[]
        for i in tdlist:
            rowlist.append(i.text) #只获取其显示文本     
        tablelist.append(rowlist)
    return tablelist

page_num=20 #定义要爬取的页数
resultlist=[]
for i in range(page_num):
    url='http://www.12365auto.com/zlts/0-0-0-0-0-0_0-0-' + str(i+1) + '.shtml'#url地址累加
    soup = requesturl(url)
    resultlist=resultlist+parsesoup(soup)#将每页获取到的列表进行相加（行数上追加）
df = pd.DataFrame(resultlist,columns=['id','brand','car_model','type','desc','problem','datetime','status'])
df.to_csv('Automotive_Quality_Information.csv',encoding="GBK")