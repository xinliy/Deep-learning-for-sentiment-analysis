import numpy as np
import pandas as pd
import collect_method




c=[movie for url in collect_method.get_top100_url_list()
   for movie in collect_method.get_top100_movie_name_list(url)]


print(np.array(c).shape)
print(c)
