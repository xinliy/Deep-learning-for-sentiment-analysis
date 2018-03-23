
import pandas as pd
import keras
import numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer



max_feature=4000
df=pd.read_csv('finalSet.csv')
tf_vec=TfidfVectorizer(ngram_range=(1,2),max_features=max_feature,stop_words='english')

x=tf_vec.fit_transform(df.review)
y=df.label

#k fold

kfold=StratifiedKFold(n_splits=5,shuffle=True,random_state=2)
cvscores=[]
for train,test in kfold.split(x,y):


    model=keras.models.Sequential()
    model.add(keras.layers.Dense(128,input_dim=max_feature))
    model.add(keras.layers.Dropout(0.3))
    model.add(keras.layers.Dense(256))
    model.add(keras.layers.Dense(1,activation='sigmoid'))
    model.summary()

    model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['acc'])
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
