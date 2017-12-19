from urllib.request import urlopen
from urllib.error import HTTPError


from bs4 import BeautifulSoup
import pandas as pd

from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool


class web_spider(object):

    def __init__(self,  movie_list, page_range=50):
        self.page_range = page_range
        self.movie_list = movie_list
        self.review_container = pd.DataFrame()
        self.url_list = []

    def get_all_url(self):

        print(self.movie_list)
        for movie in self.movie_list:
            url = 'https://www.rottentomatoes.com/m/' + movie + '/reviews'
            for i in range(1, self.page_range):
                page_number = str(i)
                url_link = url + "/?page=" + page_number + "&type=user" + "&sort="
                self.url_list.append(url_link)

    def start_collecting_data(self, number_of_worker=10):

        def collect_review(self, html, MAX_LENGTH=300):

            url_content = BeautifulSoup(html, 'html.parser')

            # Get the framework for every user's review
            for review_box in url_content.find_all('div', class_='col-xs-16'):

                # The content of the review
                review = review_box.find(
                    'div', class_='user_review').get_text().lstrip()
                review_length = len(review)

                # Count the length of stars (0-5)
                star_counter = len(review_box.find_all(
                    'span', class_='glyphicon glyphicon-star'))

                # Take 5-star-review as a positive review
                if(star_counter == 5 and review_length <= MAX_LENGTH):
                    print("Positive review!")

                    # Add the positive entry to df
                    self.recorder.append(
                        {'review': review, 'label': 1}, ignore_index=True)

                # Count the 1/2 rating benchmark (0/1)
                half_rate_counter = len(review_box.find_all(text="½"))
                if(half_rate_counter == 0):
                    half_rate_counter = len(review_box.find_all(text=" ½"))

                # print(star_counter, half_rate_counter)

                # Take 1/2 or 1 star as a negative review
                if((star_counter == 0 and half_rate_counter == 1 or
                        (star_counter == 1 and half_rate_counter == 0)) and
                   review_length <= MAX_LENGTH):
                    print("Negative review!")

                    # Add the negative entry to df
                    self.recorder.append(
                        {'review': review, 'label': 0}, ignore_index=True)

        def open_url(url):

            try:
                result = urlopen(url)
                data = collect_review(result)
                print("Open:", url)
            except HTTPError:
                print("Http error ar : ", url)
            except Exception as e:
                print("ERROR happen at.", url)
                raise e

        pool = ThreadPool(number_of_worker)
        pool.map(open_url, self.url_list)
        pool.close()
        pool.join()

    def save_to_csv(self):
        self.review_container.to_csv("TEST.csv", index=False)


comedy_movie = ['baywatch_2017', 'the_house_2017', 'snatched_2017',
                'the_artist', 'ratatouille', 'the_disaster_artist',
                'submarine-2010', 'burnt', 'ted_2', 'american_ultra']


spider = web_spider(page_range=10, movie_list=comedy_movie)
spider.get_all_url()
spider.start_collecting_data()
spider.save_to_csv()
