from urllib.request import urlopen
from bs4 import BeautifulSoup

# The origin url address
url_origin = 'https://www.rottentomatoes.com/m/iron_man/reviews/'

# Loop the front 20 page to collect reviews
for i in range(1, 20):
    page_number = str(i)
    print("Start at :", page_number)
    url = url_origin + '?page=' + str(i) + '&sort='
    # Try to get the html, error means to the end.
    try:
        html = urlopen(url)
    except Exception as e:
        print("END at: ", page_number)
        break
    html_content = BeautifulSoup(html)

    # Loop every review window.
    for review in html_content.find_all('div',
                                        class_='col-xs-16 review_container'):
        # If it's a fresh tomato then it's positive.
        if(review.find_all('div', class_='review_icon icon small fresh')):
            print("It is a positive review")
        else:
            print("It is a negtive review")

        # Get the content of the review.
        review=review.find_all('div', class_='the_review')
        print(review)
        print('___________________NEXTONE___________________')
