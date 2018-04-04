import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from keras.preprocessing.text import Tokenizer

df=pd.read_csv('nbalanced_dataset.csv')

text_df=df['review']

# def count_words(x):
#     return len(x.split())
#
# text_df=text_df.map(count_words)
#
# print(text_df)
#
# sns.countplot(text_df)
# plt.title('Lengths of comments')
# plt.xlabel('Number of words')
# plt.ylabel('Number of comments')
# plt.show()

tk=Tokenizer(num_words=4000)
tk.fit_on_texts(text_df)

print(tk.word_counts)

word_frequency=list(tk.word_counts.values())
wf=sorted(word_frequency,reverse=True)[3:]

sns.countplot(wf)
plt.xlim(xmin=0,xmax=100)
plt.show()

