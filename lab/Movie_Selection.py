
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import multiprocessing
from urllib.error import HTTPError

from functools import reduce

from multiprocessing import Pool

from multiprocessing.dummy import Pool as ThreadPool

import os
import sys
sys.path.append(os.getcwd())
import collect_method

if __name__ == '__main__':

    pool = ThreadPool(5)

    pool1 = multiprocessing.Pool(processes=4)
    movies = ['baywatch_2017', 'the_house_2017', 'snatched_2017',
              'the_artist', 'ratatouille', 'the_disaster_artist',
              'submarine-2010', 'burnt', 'ted_2', 'american_ultra']
    recorder = pd.DataFrame()
    for movie in movies:

        url = 'https://www.rottentomatoes.com/m/' + movie + '/reviews'

        url_list = []

        # Choose the range of the pages
        for i in range(1, 50):

            page_number = str(i)

            print("Start at page: ", page_number)

            # Adjust the url for every loop
            url_link = url + "/?page=" + page_number + "&type=user" + "&sort="
            print('The url address is: ', url_link)

            url_list.append(url_link)
        print(url_list)

        # Open and get the html content

        # html = urlopen(url_link)
        # html_list = pool1.map(open_to_read_html, url_list)
        with Pool(5) as p:
            pd_list = p.map(collect_method.open_to_read_html, url_list)

        pool.close()
        pool.join()

        recorder = recorder.append(pd_list)
    recorder.to_csv("TEST1.csv", index=False)

# recorder.to_csv("Movie_reviews_2.csv", index=False)
