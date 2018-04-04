# from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer
# import numpy as np
#
# cv = CountVectorizer()
#
# text = [['The movie is interesting!'],
#         ['The plot is brilliant!'],
#         ['Is enjoyable to see the movie.']]
#
# text=cv.fit_transform([e[0] for e in text])
#
# print(type(text))
#
# transformer = TfidfTransformer(smooth_idf=False)
# text2=transformer.fit_transform(text)

import math
a=1.477
b=1.477**2+2+1.176**2
b=math.sqrt(b)
print(b)