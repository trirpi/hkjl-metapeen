# HKJL METAPEEN

### To start the development server
1. touch credentials.py
2. export FLASK_APP=peen
3. export DEBUG=true
4. pip install -e
5. flask run

Use gunicorn or gevent in production. (See: http://flask.pocoo.org/docs/0.10/deploying/)

### Add new site
* Create weight in `site_weights.py`
* Create crawlfunction in `crawler/crawler.py`
* If needed add site to credentials.py

#### Exemple credentials.py

    hts_username = 'trirpi'
    hts_password = 'okeisgoed'
    
More info: https://pad.hackenkunjeleren.nl/p/hkjl-metapeen-clone


