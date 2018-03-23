from langdetect import detect
import pandas as pd
from multiprocessing import Pool
import numpy as np

df=pd.read_csv('dataset.csv')
df1=pd.read_csv('balanced_dataset.csv')


zero_set=df.loc[df['label']==0]
print(zero_set.shape)
print(df1.shape)
print(pd.pivot_table(df1,values='label',index='name',aggfunc=np.sum).sort_values('label'))
# print(df.info())
# i=0
# for index,row in df.iterrows():
#     # print(row['review'])
#     try:
#         lang=detect(row.review)
#
#     except Exception as e:
#         print(e)
#         lang=' '
#     if lang!='en':
#         print(row.review)
#         df=df.drop(df.index[index])
#     i=i+1
#     print(i)
#
# print(df.info())
