from bs4 import BeautifulSoup
import requests
import re

from peen import db
from peen.orm.models import Hacker


def get_score_rm(username):
    profile_url = 'https://root-me.org/{user}'.format(user=username)

    response = BeautifulSoup(requests.get(profile_url).content, "html.parser")  # get webpage in right format
    score = response.find_all("div", class_="t-body")[0].contents[5].contents[5].contents[1].text

    return int(score)


def get_score_cs(cs_id):
    profile_url = 'https://certifiedsecure.nl/profile/{cs_id}'.format(cs_id=cs_id)

    response = BeautifulSoup(requests.get(profile_url).content, "html.parser")  # get webpage in right format
    score = re.findall(r'\d+', response.find_all("div", class_="level_progress_details")[0].text)[1]

    return int(score)


callbacks = {
    'rm': get_score_rm,
    'cs': get_score_cs,
}


def update_score(user, site=None):
    """
    update scores of a user
    :param user: User class
    :param site: site that needs to be updated (if none it updates all scores)
    :return: nothing
    """
    scores = user.scores  # list with username/id and current score
    if site is None:
        for site_key in scores:

            score = callbacks[site_key](scores[site_key][0])  # get score
            user.scores[site_key] = (user.scores[site_key][0], score)  # set new values
    else:
        score = callbacks[site](scores[site][0])  # get score
        user.scores[site] = (user.scores[site][0], score)  # set new values

    db.session.commit()  # and put them in the db

