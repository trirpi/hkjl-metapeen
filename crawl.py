#!/usr/bin/env python

from crawler.crawler import update_all_scores, update_total_score
from peen.orm.models import Hacker

hackers = Hacker.query.all()


for hacker in hackers:
    if hacker.username == 'aczid' or hacker.username == 'sling':
        update_all_scores(hacker)
        update_total_score(hacker)
