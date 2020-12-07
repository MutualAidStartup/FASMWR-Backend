# FASMWR-Backend

Steps to create and run a virtual environment
$ virtualenv env
$ source ./env/bin/activate

Steps to install requirements
$ pip3 install -r requirements.txt

How to run the server
$ cd fasmwr
$ flask run

HOW TO CALL ROUTES
Use GET or POST requests to the server, reference here:
https://blog.miguelgrinberg.com/post/how-to-create-a-react--flask-project

<!-- Database -->

Steps to setup the database - https://realpython.com/flask-by-example-part-2-postgres-sqlalchemy-and-alembic/
$ psql
/# create database fasmwr_db;
/# \q
- config.py line 9 -> Set your secret key - DO NOT PUSH THIS TO GIT - NOTE: This file is not by default in .gitignore since you need a local copy
$ export FASMWR_DATABASE_URL="postgresql://postgres:YOURPASSWORDHERE@localhost/fasmwr_db"
$ python3 create_db.py

# migrate the database - how to update the models.py without destroying and re-creating the database
$ python manage.py db migrate
$ python manage.py db upgrade