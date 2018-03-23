import keras
import pandas as pd
from keras.preprocessing.text import one_hot
from sklearn.feature_extraction.text import  TfidfVectorizer

df=pd.read_csv('finalSet.csv')

max_feature=8000

tf_vec=TfidfVectorizer(ngram_range=(1,3),max_features=max_feature,stop_words='english')

x=tf_vec.fit_transform(df.review)
y=df.label

model=keras.models.Sequential()
model.add(keras.layers.Dense(128,input_dim=max_feature))

model.add(keras.layers.Dense(1,activation='sigmoid'))

model.compile(optimizer='rmsprop',loss='binary_crossentropy',metrics=['acc'])

result=model.fit(x,y,batch_size=128,epochs=8,validation_split=0.2)

print(result.history['val_acc'])
