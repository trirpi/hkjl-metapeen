#!/usr/bin/env python
from crawler.crawler import update_score
from peen.orm.models import Hacker

hackers = Hacker.query.all()

for hacker in hackers:
    update_score(hacker)
    hacker.update_total_score()
