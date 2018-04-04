from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
import pandas as pd
import keras
import numpy as np
from keras.layers import Dense, Input
from sklearn.model_selection import StratifiedKFold

import my_toolkit
from sklearn.feature_extraction.text import TfidfVectorizer
from keras.preprocessing import text,sequence
df = pd.read_csv('balanced_dataset.csv')
train = df.review
y = df.label

max_feature = 4000

print('1')
maxlen=50
embed_size=400

tokenizer=text.Tokenizer(num_words=max_feature,lower=True)
tokenizer.fit_on_texts(list(train))


train=tokenizer.texts_to_sequences(train)
train=sequence.pad_sequences(train,maxlen=maxlen)
x = train
print(x)
print('2')

kfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=2)
print('3')
cvscores = []
for train, test in kfold.split(x, y):
    multi_nb = MultinomialNB()
    svm1 = svm.LinearSVC()

    multi_nb.fit(x[train], y[train])
    svm1.fit(x[train], y[train])
    print('4')
    inp = Input(shape=(50,))
    s = Dense(128)(inp)
    out = Dense(1, activation='sigmoid')(s)
    model = keras.models.Model(inp, out)

    model.summary()

    model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['acc'])
    batch_size = 500

    epochs = 1

    result = model.fit(x[train], y[train], validation_data=(x[test], y[test]), batch_size=batch_size, epochs=epochs)
    cvscores.append(result.history['val_acc'])
    y_pred1 = model.predict(x[test])
    y_pred2 = multi_nb.predict_proba(x[test])
    y_pred3 = svm1.predict(x[test])
    y_pred = (y_pred1 + y_pred2 + y_pred3) / 3

    print("The precision for negative label is: ", my_toolkit.negative_precision(y[test], y_pred))

import matplotlib.pyplot as plt

print(cvscores)
for score in cvscores:
    plt.plot(score)

plt.title('val_acc')
plt.ylabel('acc')
plt.xlabel('epoch')
# plt.legend(['train','validation'],loc='upper right')
plt.show()
score = [max(e) for e in cvscores]
print(score)
print(np.mean(score))
