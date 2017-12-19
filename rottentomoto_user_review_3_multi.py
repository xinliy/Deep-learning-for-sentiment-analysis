from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
from urllib.error import HTTPError

from multiprocessing import pool
from multiprocessing.dummy import Pool as ThreadPool

pool = ThreadPool(5)


action_movie = ['hacksaw_ridge', 'blood_father', 'deepwater_horizon',
                'in_a_valley_of_violence', 'the_magnificent_seven_2016', 'dont_mess_with_texas_2014',
                'last_airbender', 'gigli', 'babylon_ad', 'drive_2011', 'fantastic_four_2015', 'mortdecai']


romance_movie = ['perfect_man', 'everything_everything_2017',
                 'lost_in_translation', 'enough_said_2013', 'up_in_the_air_2009',
                 'obvious_child', 'the_duke_of_burgundy', 'la_la_land', 'me_before_you', 'blue_is_the_warmest_color']

mystery_movie = ['paranoia_2013', 'mobsters',
                 'the_book_of_henry', 'argo_2012',
                 'arrival_2016', 'skyfall',
                 'kingsman_the_secret_service', 'a_most_wanted_man',
                 'the_drop', 'gone_girl']

comedy_movie = ['baywatch_2017', 'the_house_2017', 'snatched_2017',
                'the_artist', 'ratatouille', 'the_disaster_artist',
                'submarine-2010', 'burnt', 'ted_2', 'american_ultra']

horror_movie = ['the_dark_tower_2017', 'the_mummy_2017', 'wish_upon',
                'get_out', 'the_babadook', 'pans_labyrinth', 'the_loved_ones_2012',
                'the_conjuring_2', 'the_shallows', 'lights_out_2016', 'ouija_origin_of_evil']

movie_book = {'action_movie': action_movie, 'romance_movie': romance_movie,
              'mystery_movie': mystery_movie, 'comedy_movie': comedy_movie, 'horror_movie': horror_movie}
movie_book1 = {
    'mystery_movie': mystery_movie, 'comedy_movie': comedy_movie, 'horror_movie': horror_movie}
# The target movie reviews from the user


for movie_type, movies in movie_book.items():

    # Build pd dataframe
    recorder = pd.DataFrame()

    for movie in movies:

        url = 'https://www.rottentomatoes.com/m/' + movie + '/reviews'

        # Set max length of the review
        MAX_LENGTH = 300

        url_list = []

        # Choose the range of the pages
        for i in range(1, 10):

            page_number = str(i)

            print("Start at page: ", page_number)

            # Adjust the url for every loop
            url_link = url + "/?page=" + page_number + "&type=user" + "&sort="
            print('The url address is: ', url_link)

            url_list.append(url_link)

        def open_to_read_html(url):
            try:
                result = urlopen(url)
                return result.read()
            except HTTPError:
                print("HTTPError at: ", url)
            except Exception as e:
                print("ERROR")
            # Open and get the html content

            # html = urlopen(url_link)
        html_list = pool.map(open_to_read_html, url_list)
        pool.close()
        pool.join()


        for html in html_list:
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
                    recorder = recorder.append(
                        {'review': review, 'label': 1, 'name': movie}, ignore_index=True)

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
                    recorder = recorder.append(
                        {'review': review, 'label': 0, 'name': movie}, ignore_index=True)

                    # print(review)

                # print("________________THIS REVIEW FINISHED__________________")
        print(recorder.head(5))

    recorder.to_csv(movie_type + ".csv", index=False)

# recorder.to_csv("Movie_reviews_2.csv", index=False)
