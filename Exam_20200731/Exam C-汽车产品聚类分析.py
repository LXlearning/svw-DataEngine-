#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn import preprocessing
from scipy.cluster.hierarchy import dendrogram, ward
from sklearn.cluster import AgglomerativeClustering
import matplotlib.pyplot as plt


# In[16]:


def Competitive_product(data,index,VW_index,VW_name):
    '''vokswagen汽车的相应竞品'''
    VW = data['CarName'][index-1] # 当前VW品牌车名
    
    label_kmeans = data[data['car_ID']== index]['聚类结果'].values                       # 聚类结果
    Cp_name = data.groupby(['聚类结果']).get_group(int(label_kmeans))['CarName'].values  # 类别内所有车型
    Cp_name = list(set(Cp_name).difference(set(VW_name)))                                # 求Cp_name中有而vw_index中没有的值（竞品）
    print('%r %r 产品竞品—— %r'%(index,VW,Cp_name))

def main():
    data = pd.read_csv('./ProjectC/CarPrice_Assignment.csv')#, header = None

    ## 类别标签
    train_x = data.iloc[:,1:]

    category_col = ['CarName','fueltype','aspiration','doornumber','carbody','drivewheel',
                    'enginelocation','enginetype','cylindernumber','fuelsystem']
    dummies_df = pd.get_dummies(data[category_col],drop_first=True) 
    train_x = train_x.drop(category_col,axis=1)

    train_x = pd.concat([train_x,dummies_df],axis=1)


    ## 归一化
    min_max_scaler=preprocessing.MinMaxScaler()
    train_x=min_max_scaler.fit_transform(train_x)

    ## K-means聚类
    kmeans = KMeans(n_clusters=10)
    kmeans.fit(train_x)
    predict_y = kmeans.predict(train_x)
    # 合并聚类结果，插入到原数据中
    result = pd.concat((data,pd.DataFrame(predict_y)),axis=1)
    result.rename({0:u'聚类结果'},axis=1,inplace=True)
    # VW品牌索引、名称
    VW_index = result['car_ID'][182:194].values
    VW_name = result['CarName'][182:194].values

    # 输出相应竞品
    for i in VW_index:
        Competitive_product(result,i,VW_index,VW_name)
#         print('*'*150)
        print("\n"*2,end="")


# In[17]:


if __name__ == '__main__':
    main()


# In[ ]:




