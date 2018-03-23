import pandas as pd


df1=pd.read_csv('100.csv')
print(df1['label'].value_counts())
df2=df1.loc[df1['label']==0]
df3=df1.loc[df1['label']==1][:1817]
print(df3['label'].value_counts())
df4=pd.concat([df2,df3])
print(df4['label'].value_counts())

df4.to_csv('action_selected.csv',index=False)
# print(df2)
