import pandas as pd

from string import punctuation

from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier

import collect_method
import re

dataset=pd.read_csv('balanced_dataset.csv')






#




# data = pd.read_csv('lab/action_selected.csv',encoding='latin1')

sentence_list = []


def clean_doc(doc):
    # split into tokens by white space
    doc = doc.lower()
    tokens = doc.split()

    # remove punctuation from each token
    table = str.maketrans('', '', punctuation)
    tokens = [w.translate(table) for w in tokens]
    # remove remaining tokens that are not alphabetic
    tokens = [word for word in tokens if word.isalpha()]
    # filter out stop words
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]
    # filter out short tokens
    tokens = [word for word in tokens if len(word) > 1]

    # st = SnowballStemmer(language='english')
    # tokens = [st.stem(word) for word in tokens]
    return tokens

def list_to_string(list1):
    return " ".join(str(e) for e in list1)

# dataset.review=dataset.review.apply(clean_doc)
# dataset.review=dataset.review.apply(list_to_string)
# dataset.to_csv('finalSet.csv',index=False)
# print(dataset.head())
data=dataset


# print('Start cleaning')
# for sentence in data.review:
#     sentence = clean_doc(sentence)
#     sentence_list.append(sentence)
#
# print(" Finish cleaning")
# #
# for sentence in data.review:
#     sentence_list.append(sentence)

# vec = CountVectorizer(min_df=1, lowercase=True,stop_words='english')
tf_vec=TfidfVectorizer(ngram_range=(1,3),max_features=4000,stop_words='english')

# print(sentence_list)
# data_vectorized = vec.fit_transform(data.review)

# print(data_vectorized.A)

train=tf_vec.fit_transform(data.review)



classifier = MultinomialNB()

svm = svm.LinearSVC()

random_forest = RandomForestClassifier()

#
# train = data_vectorized.A
label = data.label
X = train
y = label

print(train)





score='accuracy'
import time
start=time.time()

score1 = cross_val_score(classifier, train, label, cv=4, scoring=score)
print('Time one: ',time.time()-start)
score2 = cross_val_score(svm, train, label, cv=4, scoring=score)
print('Time two: ',time.time()-start)

score3=cross_val_score(random_forest,train,label,cv=4,scoring=score)
print('Time three: ',time.time()-start)



print(score1.mean())
print(score2.mean())
print(score3.mean())
