
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import multiprocessing
from urllib.error import HTTPError

import re


def extract_name_from_url(url):
    return re.search(r'/m.*/reviews', url).group(0).split("/")[2]


def open_to_read_html(url, MAX_LENGTH=300):

    movie_name = extract_name_from_url(url)
    # print(movie_name)
    instant_df = pd.DataFrame()

    try:
        html = urlopen(url)
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
                instant_df = instant_df.append(
                    {'review': review, 'label': 1, 'name': movie_name}, ignore_index=True)

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
                instant_df = instant_df.append(
                    {'review': review, 'label': 0, 'name': movie_name}, ignore_index=True)
        print(instant_df.shape)
        return instant_df

    except HTTPError:
        print("HTTPError at: ", url)
    except Exception as e:
        print("ERROR")
        raise e
