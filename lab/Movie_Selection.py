
import pandas as pd
import multiprocessing
from multiprocessing import Pool


# Add local method, otherwise Pool will raise error
import os
import sys
sys.path.append(os.getcwd())
import collect_method

# Add main function, otherwise Pool will rasie error
if __name__ == '__main__':

    movies = ['baywatch_2017', 'the_house_2017', 'snatched_2017',
              'the_artist', 'ratatouille', 'the_disaster_artist',
              'submarine-2010', 'burnt', 'ted_2', 'american_ultra']
    recorder = pd.DataFrame()
    for movie in movies:

        url = 'https://www.rottentomatoes.com/m/' + movie + '/reviews'

        # Add multi threds to speed up.
        with Pool(15) as p:
            pd_list = p.map(collect_method.open_to_read_html,
                            collect_method.create_url_list(url))
        recorder = recorder.append(pd_list)
    recorder.to_csv("TEST1.csv", index=False)

# recorder.to_csv("Movie_reviews_2.csv", index=False)
