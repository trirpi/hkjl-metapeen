# HKJL METAPEEN

## Start server

Clone project.

1. git clone https://github.com/trirpi/hkjl-metapeen
2. cd hkjl-metapeen

Create virtual evironment.

3. virtualenv -p python3 metapeen
4. source metapeen/bin/activate

Install dependencies.

5. pip install -r requirements.txt

Set mode to development or production. (if you don't do this, it will default to development)

6. export FLASK_CONFIG=development

Create database and admin.

7. python manage.py setup

Start Flask.

8. python run.py


#### Exemple credentials.py

    ht = { 
        'username': 'fgt123',
        'hts_password': 'okeisgoed'
    }


## Architecture

There are two main parts:

- The website (hkjl-metapeen/peen)
- The crawler (hkjl-metapeen/crawler)

### The website
The website has an index page where all the scores are listed. And there is an admin interface.
The scores are fetched from a sqlite db (this can become redis or something other later).
The db has 3 tables:

- Hacker: users with there scores and usernames of ctf sites
- User: an admin user (or maybe more then one)
- Account: account of hackers (specific site, current score, specific username)
##### Index page
Currently shows exactly what is in the db.

##### Admin interface
Currently lists all hackers

#### API
    /api/user/<id>
returns user

    /api/users
returns list of all users

### The crawler
This updates all the scores of the users. Should be ran by cron every hour or so.
I am working on this.


More info: https://pad.hackenkunjeleren.nl/p/hkjl-metapeen-clone
