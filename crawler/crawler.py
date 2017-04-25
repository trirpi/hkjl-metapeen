from bs4 import BeautifulSoup
import requests
import re

from peen import db


def get_score_rm(username):
    profile_url = 'https://root-me.org/{user}'.format(user=username)

    response = BeautifulSoup(requests.get(profile_url).content, "html.parser")  # get webpage in right format
    try:
        score = response.find_all("div", class_="t-body")[0].contents[5].contents[5].contents[1].text
        return int(score)
    except IndexError:
        return None


def get_score_cs(cs_id):
    profile_url = 'https://certifiedsecure.nl/profile/{cs_id}'.format(cs_id=cs_id)

    response = BeautifulSoup(requests.get(profile_url).content, "html.parser")  # get webpage in right format
    try:
        score = re.findall(r'\d+', response.find_all("div", class_="level_progress_details")[0].text)[1]
        return int(score)
    except IndexError:
        return None


def get_score_otw(wechall_username):
    profile_url = 'https://www.wechall.net/profile/{wechall_username}'.format(wechall_username=wechall_username)

    response = BeautifulSoup(requests.get(profile_url).content, "html.parser")
    table = response.find_all("table")[1]
    for words in table.contents:
        if 'OverTheWire.org' in str(words):
            try:
                return int(re.findall(r'\d+', str(words.contents[2]))[0])
            except IndexError:  # niet gevonden ofzo
                return None


callbacks = {
    'rm': get_score_rm,
    'cs': get_score_cs,
    'otw': get_score_otw
}


def update_score(hacker, site=None):
    """
    update scores of a user
    :param hacker: Hacker class instance
    :param site: site that needs to be updated (if none it updates all scores)
    :return: nothing
    """
    scores = hacker.scores  # list with username/id and current score
    if site is None:
        for site_key in scores:

            score = callbacks[site_key](scores[site_key][0])  # get score
            hacker.scores[site_key] = (hacker.scores[site_key][0], score)  # set new values
    else:
        score = callbacks[site](scores[site][0])  # get score
        hacker.scores[site] = (hacker.scores[site][0], score)  # set new values

    db.session.commit()  # and put them in the db

