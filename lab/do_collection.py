import pandas as pd
import multiprocessing
from multiprocessing import Pool
import re

# Add local method, otherwise Pool will raise error

import collect_method

# Add main function, otherwise Pool will rasie error
if __name__ == '__main__':

    # c = [movie for url in collect_method.get_top100_url_list()
    #      for movie in collect_method.get_top100_movie_name_list(url)]

    # movies = ['baywatch_2017', 'the_house_2017', 'snatched_2017',
    #           'the_artist', 'ratatouille', 'the_disaster_artist',
    #           'submarine-2010', 'burnt', 'ted_2', 'american_ultra']
    url = 'https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/'

    for url in collect_method.get_top100_url_list():

        movies = [movie for movie in collect_method.get_top100_movie_name_list(url)]
        # Get the theme of the movies
        theme = re.search(r'100_.*_movies/', url).group(0).replace('100_', '').replace('_movies/', '')
        print(theme)

        # movies=[movie for movie in collect_method.get_top100_movie_name_list(url)]
        recorder = pd.DataFrame()
        for count, movie in enumerate(movies, 1):
            url = 'https://www.rottentomatoes.com/m/' + movie + '/reviews'

            # Add multi threds to speed up.
            with Pool(5) as p:
                pd_list = p.map(collect_method.open_to_read_html,
                                collect_method.create_url_list(url))
            recorder = recorder.append(pd_list)
            # Every 10 iteration make a csv file.
            if count % 10 == 0:
                recorder.to_csv(theme + str(count) + ".csv", index=False)
                print("The data is recorded at count: ", count)
                print('The theme now is :',theme)
        recorder.to_csv(theme + ".csv", index=False)
