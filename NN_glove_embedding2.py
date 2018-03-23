
import pandas as pd
import keras
import numpy as np
from keras.preprocessing import text, sequence
from keras.layers import Dense,MaxPooling1D,Input,LSTM,Bidirectional,Conv1D,GRU,Dropout,Embedding,GlobalMaxPool1D
from keras.models import Sequential

df=pd.read_csv('finalSet.csv')
train=df.review
y=df.label
EMBEDDING_FILE='glove.840B.300d.txt'

max_feature=2000
maxlen=150
embed_size=300

tokenizer=text.Tokenizer(num_words=max_feature,lower=True)
tokenizer.fit_on_texts(list(train))


train=tokenizer.texts_to_sequences(train)
train=sequence.pad_sequences(train,maxlen=maxlen)

# embeddings_index={}
#
# with open(EMBEDDING_FILE,encoding='utf8') as f:
#     for line in f:
#         values=line.rstrip().rsplit(' ')
#         word=values[0]
#         coefs=np.asarray(values[1:],dtype='float32')
#         embeddings_index[word]=coefs
#
# word_index=tokenizer.word_index

# num_words=min(max_feature,len(word_index)+1)
# embedding_matrix=np.zeros((num_words,embed_size))
# for word, i in word_index.items():
#     if i >=max_feature:
#         continue
#
#     embedding_vector=embeddings_index.get(word)
#
#     if embedding_vector is not None:
#         embedding_matrix[i]=embedding_vector

# inp=Input(shape=(maxlen,))
#
# x=Embedding(max_feature,embed_size,weights=[embedding_matrix],trainable=True)(inp)
#
# x=Conv1D(64,kernel_size=3,padding='valid',kernel_initializer='glorot_uniform')(x)
# max_pool=GlobalMaxPool1D()(x)
#
# out=Dense(1,activation='sigmoid')(max_pool)
#
# model=keras.models.Model(inp,out)
model=Sequential()
model.add(Embedding(max_feature,100,input_length=maxlen))
# model.add(Conv1D(128,3))
# model.add(keras.layers.LSTM(32))
model.add(keras.layers.Bidirectional(GRU(24)))
# model.add(MaxPooling1D(3))
# model.add(Conv1D(64,3))
# model.add(GlobalMaxPool1D())
model.add(Dense(1,activation='sigmoid'))
model.summary()

model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['acc'])
batch_size=2000

epochs=12


result=model.fit(train,y,batch_size=batch_size,epochs=epochs,validation_split=0.1)

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
