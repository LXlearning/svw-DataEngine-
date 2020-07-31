#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
from efficient_apriori import apriori

from mlxtend.frequent_patterns import apriori as api
from mlxtend.frequent_patterns import association_rules

def main():
    product = pd.read_csv('./ProjectB/产品表.csv',encoding='ANSI')
    order = pd.read_csv('./ProjectB/订单表.csv',encoding='ANSI')
    customer = pd.read_csv('./ProjectB/客户.csv',encoding='ANSI')
    date = pd.read_csv('./ProjectB/日期表.csv',encoding='ANSI')

    transactions = [] #频繁项集数据集
    for name,group in order.groupby('客户ID'):
        cus_list = group['产品名称'].unique().tolist() #每个客户购买的产品
        transactions.append(cus_list)

    itemsets, rules = apriori(transactions, min_support=0.02,  min_confidence=0.4)
    print("频繁项集：", itemsets)
    print("关联规则：", rules)


# In[4]:


if __name__ == '__main__':
    main()


# In[ ]:




