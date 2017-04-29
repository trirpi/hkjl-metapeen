# HKJL METAPEEN

### To start the development server
1. touch credentials.py
2. export FLASK_APP=peen
3. export DEBUG=true
4. pip install -e
5. flask run

Use gunicorn or gevent in production. (See: http://flask.pocoo.org/docs/0.10/deploying/)


#### Exemple credentials.py

    hts = { 
        'username': 'trirpi',
        'hts_password': 'okeisgoed'
    }


## Architecture

There are two main parts:

- The website (hkjl-metapeen/peen)
- The crawler (hkjl-metapeen/crawler)

### The website
The website has an index page where all the scores are listed. And there is an admin interface.
The scores are fetched from a sqlite db (this can become redis or something other later).
The db has 2 tables:

- Hacker: users with there scores and usernames of ctf sites
- User: an admin user (or maybe more then one)

##### Index page
Currently shows exactly what is in the db.

##### Admin interface
Currently lists all hackers

### The crawler
This updates all the scores of the users. Should be ran by cron every hour or so.
I am working on this.


More info: https://pad.hackenkunjeleren.nl/p/hkjl-metapeen-clone


