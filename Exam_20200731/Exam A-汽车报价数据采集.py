#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

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
    temp = soup.find_all("p",class_='cx-name text-hover')
    name,price,image = [],[],[]
    
    for i in temp:
        name.append(i.text) # 去除标签,汽车名称
    temp2 = soup.find_all("p",class_='cx-price')
    for i in temp2:
        price.append(i.text) # 价格区间
    temp3 = soup.find_all("img",class_='img')
    for i in temp3:
        image.append(i['src']) # 图片链接    
        
    # 爬取数据处理
    result = pd.DataFrame(columns=['名称','最低价格(万)','最高价格(万)','产品图片链接'])
    for i in range(len(price)):
        df ={}
        df['名称'] = name[i]
        if price[i] == '暂无':
            df['最低价格(万)'] = np.NaN
            df['最高价格(万)'] = np.NaN
        elif '-' in price[i]:
            df['最低价格(万)'] = float(price[i].split('-')[0])
            df['最高价格(万)'] = float(price[i].split('-')[1][:-1])
        else:
            df['最低价格(万)'] = float(price[i][:-1])
            df['最高价格(万)'] = float(price[i][:-1])
        df['产品图片链接'] = 'http:'+ image[i]
        result = result.append(df,ignore_index=True)
    return result

def main():
    """
        Action：汽车报价数据采集：
        数据源：易车网大众品牌汽车http://car.bitauto.com/xuanchegongju/?l=8&mid=8
        字段：  名称，最低价格，最高价格，产品图片链接
    """

    result =  pd.DataFrame()
    page_num=3 #定义要爬取的页数
    for i in range(page_num):
        url='http://car.bitauto.com/xuanchegongju/?mid=8&page=' + str(i+1)#url地址累加
        soup = requesturl(url)
        result = result.append(parsesoup(soup))#将每页获取到的列表进行相加（行数上追加）

    result = result.reset_index(drop=True) #索引重排
    result.to_csv('Price_VW.csv',encoding="GBK")


# In[2]:


if __name__ == '__main__':
    main()


# In[ ]:




