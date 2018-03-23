
import pandas as pd
import keras
import numpy as np
from keras.preprocessing import text, sequence
from keras.layers import Dense,MaxPooling1D,Input,LSTM,Bidirectional,Conv1D,GRU,Dropout,Embedding,GlobalMaxPool1D
from keras.models import Sequential
from sklearn.model_selection import StratifiedKFold
import numpy


df=pd.read_csv('finalSet.csv')
train=df.review
y=df.label

max_feature=4000
maxlen=50

tokenizer=text.Tokenizer(num_words=max_feature,lower=True)
tokenizer.fit_on_texts(list(train))


train=tokenizer.texts_to_sequences(train)
train=sequence.pad_sequences(train,maxlen=maxlen)
x=train
#k fold

kfold=StratifiedKFold(n_splits=5,shuffle=True,random_state=2)
cvscores=[]
for train,test in kfold.split(x,y):

    model=keras.models.Sequential()
    model.add(Embedding(max_feature,300,input_length=maxlen))
    # model.add(Conv1D(128,3))
    # model.add(keras.layers.LSTM(32))
    model.add(keras.layers.Bidirectional(GRU(128,return_sequences=True)))
    model.add(Conv1D(128,3))
    model.add(GlobalMaxPool1D())
    model.add(Dense(64))
    model.add(Dense(1,activation='sigmoid'))
    model.summary()

    model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['acc'])
    batch_size=500

    epochs=4


    result=model.fit(x[train],y[train],validation_data=(x[test],y[test]),batch_size=batch_size,epochs=epochs,validation_split=0.1)
    cvscores.append(result.history['val_acc'])

import matplotlib.pyplot as plt
print(cvscores)
plt.plot(cvscores)
plt.title('model train vs validation acc')
plt.ylabel('acc')
plt.xlabel('epoch')
# plt.legend(['train','validation'],loc='upper right')
plt.show()
score=[max(e) for e in cvscores]
print(score)
print(np.mean(score))
