import pandas as pd
import numpy as np

from string import punctuation

from nltk.corpus import stopwords

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.naive_bayes import MultinomialNB
from sklearn import svm
from sklearn.model_selection import cross_val_score
from sklearn.ensemble import RandomForestClassifier
import lightgbm as lgb

from sklearn.model_selection import StratifiedKFold


data = pd.read_csv(
    "data/['the_dark_tower_2017', 'the_mummy_2017', 'wish_upon', 'get_out', 'the_babadook', 'pans_labyrinth', 'the_loved_ones_2012'].csv", encoding='latin1')

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

svm = svm.LinearSVC()

random_forest = RandomForestClassifier()

lgb_model = lgb.LGBMClassifier()

train = data_vectorized.A
label = data.label
X = train
y = label

print(train)

score1 = cross_val_score(classifier, train, label, cv=4, scoring='accuracy')
score2 = cross_val_score(svm, train, label, cv=4, scoring='accuracy')
# score3=cross_val_score(random_forest,train,test,cv=4,scoring='accuracy')


def gini(y, pred):
    g = np.asarray(np.c_[y, pred, np.arange(len(y))], dtype=np.float)
    g = g[np.lexsort((g[:, 2], -1 * g[:, 1]))]
    gs = g[:, 0].cumsum().sum() / g[:, 0].sum()
    gs -= (len(y) + 1) / 2.
    return gs / len(y)


def gini_lgb(preds, dtrain):
    y = list(dtrain.get_label())
    score = gini(y, preds) / gini(y, y)
    return 'gini', score, True

lgb_dataset = lgb.Dataset(train, label=label)
lgb_params = {'metric': 'accuracy', 'learning_rate': 0.02, 'max_depth': 10, 'num_leaves': 500, 'max_bin': 10, 'objective': 'binary',
              'feature_fraction': 0.8, 'bagging_fraction': 0.9, 'bagging_freq': 10}

kfold = 5
nrounds = 1000
skf = StratifiedKFold(n_splits=5, random_state=1)
for i, (train_index, test_index) in enumerate(skf.split(X, y)):
    print('lgb kfold:{} of {}:'.format(i + 1, kfold))
    X_train, X_eval = X[train_index], X[test_index]
    y_train, y_eval = y[train_index], y[test_index]
    lgb_model = lgb.train(lgb_params, lgb.Dataset(X_train, label=y_train), nrounds, lgb.Dataset(
        X_eval, label=y_eval), verbose_eval=100, feval=gini_lgb, early_stopping_rounds=100)

print(score1.mean())
print(score2.mean())
