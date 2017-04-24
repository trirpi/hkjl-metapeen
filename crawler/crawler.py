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


def update_score(username, site):
    user = Hacker.query.filter_by(username=username).first()  # get correct user
    scores = user.scores  # list with username/id and current score

    score = callbacks[site](scores[site][0])  # get score

    user = Hacker.query.filter_by(username=username).first()  # get correct user
    user.scores[site] = (user.scores[site][0], score)  # set new values
    db.session.commit()  # and put them in the db

update_score('trirpi', 'cs')

