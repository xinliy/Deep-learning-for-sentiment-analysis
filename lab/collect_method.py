
2
from bs4 import BeautifulSoup
import pandas as pd
from urllib.error import HTTPError

import re

'''
  Return a list of top100 movie url
'''
def get_top100_url():

    return ['https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_animation_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_art_house__international_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_classics_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_comedy_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_documentary_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_drama_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_horror_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_kids__family_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_musical__performing_arts_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_mystery__suspense_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_romance_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_science_fiction__fantasy_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_special_interest_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_sports__fitness_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_television_movies/',
    'https://www.rottentomatoes.com/top/bestofrt/top_100_western_movies/']


def get_movie_dict():

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
    return movie_book

'''
  Depend on the url extract the movie name.
  :params str url: Input url
  :return str : The movie name
'''
def extract_name_from_url(url):
    return re.search(r'/m.*/reviews', url).group(0).split("/")[2]

'''
  Read the html and extract the pos/neg reviews
  params: str url: the url address
  params: int MAX_LENGTH(Default:300): the max length for each review
  return: pd.DataFrame: a df contains all the reviews, with label and movie name

'''
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

  '''
  Use url to create all the links of the reviews.

  :param str url: The origin url address 
  :param int MAX_RANGE: The max range of page for the movie
  :return list url_list: A list of url in string
  '''
def create_url_list(url, MAX_RANGE=50):
    url_list = []
    for page in range(1, 50):
        page_number = str(page)
        url_link = url + "/?page=" + page_number + "&type=user" + "&sort="
        url_list.append(url_link)
    print(url_list)
    return url_list



'''
  Get the name of top 100 movie name
  :param str url: the origin address
  :return list movie_list: a list contains all the movie names

'''

def get_top100_movie_list(url):
    open_url = urlopen(url)

    html = BeautifulSoup(open_url, 'html.parser')
    movie_list = []
    for a in html.find('table', class_="table").find_all("a", href=True):
        href = a['href']

        true_href = re.search(r'm/.*', href)
        # group() will rasie error if not found
        try:
            movie_name = true_href.group(0).split("/")[1]
            movie_list.append(movie_name)

        except Exception as e:
            pass

    movie_list = list(set(movie_list))
    print(movie_list)
    return movie_list
