import numpy as np
from keras.datasets import imdb
from matplotlib import pyplot
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Flatten
from keras.layers.embeddings import Embedding
from keras.preprocessing import sequence


(X_train, y_train),(X_test,y_test)=imdb.load_data()
X=np.concatenate((X_train,X_test),axis=0)
y=np.concatenate((y_train,y_test),axis=0)

print("shape")
print(X.shape)
print(y.shape)

top_words=5000
imdb.load_data(num_words=5000)
(X_train,y_train),(X_test,y_test)=imdb.load_data(num_words=top_words)

max_words=500

X_train=sequence.pad_sequences(X_train,maxlen=max_words)
X_test=sequence.pad_sequences(X_test,maxlen=max_words)

Embedding(5000,32,input_length=500)

model = Sequential()
model.add(Embedding(top_words,32,input_length=max_words))
model.add(Flatten())
model.add(Dense(250,activation='relu'))	
model.add(Dense(1,activation='sigmoid'))
model.compile(loss='binary_crossentropy',optimizer='adam',metrics=['accuracy'])
print(model.summary())

model.fit(X_train,y_train,validation_data=(X_test,y_test),epochs=5,batch_size=128,verbose=4)
scores=model.evaluate(X_test,y_test,verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))