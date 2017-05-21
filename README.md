# HKJL METAPEEN

## Development server

Clone project.

1. git clone https://github.com/trirpi/hkjl-metapeen
2. cd hkjl-metapeen

Create virtual evironment.

3. virtualenv metapeen
4. source metapeen/bin/activate

Install dependencies.

5. python setup.py develop

Create database and admin.

6. python create_db.py
7. python create_admin.py

Start Flask.

8. export FLASK_APP=peen

8.b) export FLASK_DEBUG=1 (for debugging)

9. flask run

Use gunicorn or gevent in production. (See: http://flask.pocoo.org/docs/0.10/deploying/)
Also change the `SECRET_KEY` in config.py.
You can use `python -c "import uuid; print(uuid.uuid4())"` to create a random `SECRET_KEY`.

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
The db has 2 tables:

- Hacker: users with there scores and usernames of ctf sites
- User: an admin user (or maybe more then one)

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


