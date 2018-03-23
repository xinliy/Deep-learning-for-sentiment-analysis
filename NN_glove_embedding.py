
import pandas as pd
import keras
import numpy as np
from keras.preprocessing import text, sequence
from keras.layers import Dense,MaxPooling1D,Input,LSTM,Bidirectional,Conv1D,GRU,Dropout,Embedding,GlobalMaxPool1D
from keras.models import Sequential

df=pd.read_csv('balanced_dataset.csv')

train=df.review
y=df.label
#
max_feature=2000
maxlen=50
embed_size=300
#
tokenizer=text.Tokenizer(num_words=max_feature,lower=True)
tokenizer.fit_on_texts(list(train))


train=tokenizer.texts_to_sequences(train)
train=sequence.pad_sequences(train,maxlen=maxlen)
#
#
model=Sequential()
model.add(Embedding(max_feature,100,input_length=maxlen))
model.add(keras.layers.Bidirectional(GRU(24)))
model.add(Dense(1,activation='sigmoid'))
model.summary()

model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['acc'])
batch_size=500

epochs=10


result=model.fit(train,y,batch_size=batch_size,epochs=epochs,validation_split=0.2)

history=result
import matplotlib.pyplot as plt
print(result.history['val_acc'])
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model train vs validation acc')
plt.ylabel('acc')
plt.xlabel('epoch')
plt.legend(['train','validation'],loc='upper right')
plt.show()
