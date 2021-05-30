import requests
from bs4 import BeautifulSoup  # to parse HTML data to an object
import pprint

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')
mega_links = soup.select('.storylink')
mega_subtext = soup.select('.subtext')
more = soup.select('.morelink')[0].get('href')
try:
    number_of_sides = int(input('how many sides do you want to scrap? '))
    if number_of_sides > 1:
        for i in range(2, number_of_sides+1):
            more_res = requests.get(f'https://news.ycombinator.com/news?p={i}')
            more_soup = BeautifulSoup(more_res.text, 'html.parser')
            more_links = more_soup.select('.storylink')
            more_subtext = more_soup.select('.subtext')
            mega_links = mega_links + more_links
            mega_subtext = mega_subtext + more_subtext
except ValueError as err:
    raise('Error!!! ' + err)


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_costume_hn(links, subtext):
    hn = []
    for idx, item in enumerate(links):

        title = links[idx].getText()  # or use item instead of links[idx]
        href = links[idx].get('href', None)
        vote = subtext[idx].select('.score')
        if len(vote):
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'tile': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hn)


pprint.pprint(create_costume_hn(mega_links, mega_subtext))
