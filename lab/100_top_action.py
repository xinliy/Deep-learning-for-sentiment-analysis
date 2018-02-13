from urllib.request import urlopen
from bs4 import BeautifulSoup
import re



url = 'https://www.rottentomatoes.com/top/bestofrt/top_100_action__adventure_movies/'


open_url = urlopen(url)

html = BeautifulSoup(open_url, 'html.parser')
movie_list = []
for a in html.find('table',class_="table").find_all("a", href=True):
    href = a['href']
    
    true_href = re.search(r'm/.*', href)
    try:
        movie_name = true_href.group(0).split("/")[1]
        # print(true_href.group(0).split("/")[1])
        movie_list.append(movie_name)

    except Exception as e:
        pass

movie_list=list(set(movie_list))
print(movie_list)
