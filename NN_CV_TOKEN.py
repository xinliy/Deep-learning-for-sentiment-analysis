
import pandas as pd
import keras
import numpy as np
from keras.preprocessing import text, sequence
from keras.layers import Dense,MaxPooling1D,Input,LSTM,Bidirectional,Conv1D,GRU,Dropout,Embedding,GlobalMaxPool1D
from keras.models import Sequential
from sklearn.model_selection import StratifiedKFold
import numpy
import keras.backend as K


def f1(y_true,y_pred):
    def recall(y_true,y_pred):

        # Only y_true=1 and y_pred>=0.5 will be 1 and have value
        true_positives=K.sum(K.round(K.clip(y_true*y_pred,0,1)))
        possible_positives=K.sum(K.round(K.clip(y_true,0,1)))

        recall=true_positives/(possible_positives+K.epsilon())
        return  recall

    def precision(y_true,y_pred):

        true_positives=K.sum(K.round(K.clip(y_true*y_pred,0,1)))
        predicted_positives=K.sum(K.round(K.clip(y_pred,0,1)))
        precision= true_positives/(predicted_positives+K.epsilon())
        return precision

    precision=precision(y_true,y_pred)
    recall=recall(y_true,y_pred)
    return 2*((precision*recall)/(precision+recall))








df=pd.read_csv('finalSet.csv')

max_feature=4000

tokenizer=text.Tokenizer(num_words=max_feature,lower=True)
tokenizer.fit_on_texts(df.review)
x=tokenizer.texts_to_matrix(df.review)
y=df.label


#k fold

kfold=StratifiedKFold(n_splits=5,shuffle=True,random_state=2)
cvscores=[]
for train,test in kfold.split(x,y):

    model=keras.models.Sequential()
    model.add(keras.layers.Dense(16,input_dim=max_feature))
    model.add(keras.layers.Dropout(0.5))
    model.add(keras.layers.Dense(32,activation='relu'))
    model.add(keras.layers.Dense(1,activation='sigmoid'))
    model.summary()

    model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['acc',f1])
    batch_size=500

    epochs=8


    result=model.fit(x[train],y[train],validation_data=(x[test],y[test]),batch_size=batch_size,epochs=epochs)
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
