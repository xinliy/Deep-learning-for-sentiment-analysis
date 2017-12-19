from urllib.request import urlopen
from urllib.error import HTTPError


from bs4 import BeautifulSoup
import pandas as pd

from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool

recorder=pd.DataFrame()


def collect_review(html, MAX_LENGTH=300):

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
            recorder.append(
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
            recorder.append(
                {'review': review, 'label': 0}, ignore_index=True)


class multi_crawler():

    def __init__(self, movie):
        self.movie = movie
        self.container = pd.DataFrame()

    def convert_to_url(movie):
        url = 'https://www.rottentomatoes.com/m/' + movie + '/reviews'
        return url

    def convert_to_url_page_list(url, max_range=50):
        url_list = []
        for i in range(1, max_range):
        	page_number = str(i)
            url_link = url + "/?page=" + page_number + "&type=user" + "&sort="
            url_list.append(url_link)
        return url_list

    def read_url(url):

    	try:
    		html=urlopen(url)

    	except HTTPError:
            print("Http error ar : ", url)
        except Exception as e:
            print("ERROR happen at.", url)
            raise e

        return html



