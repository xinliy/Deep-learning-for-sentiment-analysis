
import pandas as pd
import keras
import numpy as np
from keras.preprocessing import text, sequence
from keras.layers import Dense,SpatialDropout1D,\
    MaxPooling1D,Input,LSTM,Bidirectional,Conv1D,Conv2D,MaxPooling2D,GlobalMaxPool2D,\
    GRU,Dropout,Embedding,GlobalMaxPool1D,GlobalAveragePooling1D,\
    concatenate,add
from keras.models import Sequential
from sklearn.model_selection import StratifiedKFold
import numpy


df=pd.read_csv('finalSet.csv')
train=df.review
y=df.label

max_feature=4000
maxlen=50
embed_size=400

tokenizer=text.Tokenizer(num_words=max_feature,lower=True)
tokenizer.fit_on_texts(list(train))


train=tokenizer.texts_to_sequences(train)
train=sequence.pad_sequences(train,maxlen=maxlen)
x=train
#k fold

kfold=StratifiedKFold(n_splits=5,shuffle=True,random_state=2)
cvscores=[]
for train,test in kfold.split(x,y):

    # inp=Input(shape=(maxlen,))
    # stream=Embedding(max_feature,embed_size)(inp)
    # stream=SpatialDropout1D(0.2)(stream)
    # stream=Bidirectional(LSTM(160,return_sequences=True))(stream)
    # stream=Conv1D(80,kernel_size=3)(stream)
    # avg_pool=GlobalAveragePooling1D()(stream)
    # max_pool=GlobalMaxPool1D()(stream)
    # stream=concatenate([avg_pool,max_pool])
    # out=Dense(1,activation='sigmoid')(stream)
    # model=keras.models.Model(inp,out)

    inp=Input(shape=(maxlen,))
    s=Embedding(max_feature,embed_size)(inp)
    s=LSTM(256,return_sequences=True)(s)
    s=Conv1D(256,5)(s)
    s=MaxPooling1D()(s)
    s=Conv1D(256,5)(s)
    s=Dense(128)(s)
    s=GlobalMaxPool1D()(s)
    out=Dense(1,activation='sigmoid')(s)
    model=keras.models.Model(inp,out)

    model.summary()

    model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['acc'])
    batch_size=500

    epochs=5


    result=model.fit(x[train],y[train],validation_data=(x[test],y[test]),batch_size=batch_size,epochs=epochs,validation_split=0.1)
    cvscores.append(result.history['val_acc'])

import matplotlib.pyplot as plt
print(cvscores)
for score in cvscores:
    plt.plot(score)

plt.title('val_acc')
plt.ylabel('acc')
plt.xlabel('epoch')
# plt.legend(['train','validation'],loc='upper right')
plt.show()
score=[max(e) for e in cvscores]
print(score)
print(np.mean(score))
