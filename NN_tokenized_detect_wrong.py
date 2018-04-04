import pandas as pd
from keras.preprocessing.text import Tokenizer
from keras.layers import Dense
import keras
from sklearn.model_selection import train_test_split


dataset=pd.read_csv('balanced_dataset.csv')
dataset.reset_index()
dataset['id']=dataset.index


num_word=4000
tk=Tokenizer(num_words=num_word)
tk.fit_on_texts(dataset.review)
x=tk.texts_to_matrix(dataset.review)
y=dataset.label

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.1,)


model=keras.models.Sequential()
model.add(Dense(128,input_dim=num_word))
model.add(Dense(1,activation='sigmoid'))

model.compile(loss='binary_crossentropy',optimizer='rmsprop',metrics=['acc'])



result=model.fit(x_train,y_train,batch_size=128,epochs=2,validation_split=0.2)

print(result.history['val_acc'])




# Get the wrong dataset
pred=model.predict(x_test)
pred=[1 if i >=0.5 else 0 for i in pred]

wrong_list=[]

i=0
for  index,value in y_test.iteritems():

    if pred[i]!=int(value):
        wrong_list.append(index)
    i=i+1

print("length of wrong: " ,len(wrong_list))

wrong_set=dataset[dataset['id'].isin(wrong_list)]
wrong_set.to_csv('wrong_set.csv',index=False)















