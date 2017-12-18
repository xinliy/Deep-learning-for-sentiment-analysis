import pandas as pd

from string import punctuation

from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.model_selection import cross_val_score


data = pd.read_csv(
    "['the_dark_tower_2017', 'the_mummy_2017', 'wish_upon', 'get_out', 'the_babadook', 'pans_labyrinth', 'the_loved_ones_2012'].csv", encoding='latin1')

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
    # st = LancasterStemmer()
    # tokens = [st.stem(word) for word in tokens]
    return tokens


for sentence in data.review:
    sentence = clean_doc(sentence)

    sentence_list.append(sentence)


for sentence in data.review:
    sentence_list.append(sentence)


vec = CountVectorizer(min_df=1, lowercase=False)


# print(sentence_list)
data_vectorized = vec.fit_transform(data.review)

print(data_vectorized.A)


classifier = MultinomialNB()

svm=svm.LinearSVC()

train = data_vectorized.A
test = data.label

print(train)
score1 = cross_val_score(classifier, train, test, cv=4,scoring='accuracy')
score2= cross_val_score(svm,train,test,cv=4,scoring='accuracy')

print(score1.mean())
print(score2.mean())
