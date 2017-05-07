"""
Scrape BeautifulSoup objects for score of user.

:Example:
>>> callbacks['rm'](bs_object)
5
"""

import re


def rm(response):
    score = response.find_all("div", class_="t-body")[0].contents[5].contents[5].contents[1].text
    return int(score)


def cs(response):
    score = re.findall(r'\d+', response.find_all("div", class_="level_progress_details")[0].text)[1]
    return int(score)


def otw(response):
    table = response.find_all("table")[1]
    for words in table.contents:  # loop over tables to find the overthewire table where the correct score is stored
        if 'OverTheWire.org' in str(words):
            return int(re.findall(r'\d+', str(words.contents[2]))[0])


def ht(response):
    spans = response.find_all("span", class_="right")
    score = spans[0].contents[0]
    return int(score)

callbacks = {
    'rm': rm,
    'cs': cs,
    'otw': otw,
    'ht': ht,
}
