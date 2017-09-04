[![Build Status](https://travis-ci.org/machariamarigi/shopping_list_api.svg)](https://travis-ci.org/machariamarigi/shopping_list_api) [![Coverage Status](https://coveralls.io/repos/github/machariamarigi/shopping_list_api/badge.svg?branch=development)](https://coveralls.io/github/machariamarigi/shopping_list_api?branch=development) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

# Shoppinglist API

Application Programming Interface for a shoppinglist app.


## Prerequisites
* [Python 3.5](https://www.python.org/downloads/release/python-350/)
* [virtualenv](https://virtualenv.pypa.io/en/stable/)(with [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) optionally)
* [Flask](http://flask.pocoo.org/)
* [Postgres](https://wiki.postgresql.org/wiki/Detailed_installation_guides)

## Database
* Swith to posgres account(using bash shell)
    ```
    sudo su - postgres
    ```
* Run PostgreSQL command line client.
    ```
    psql
    ```
* Create a database user with a password.
    ```
    CREATE USER shopping with password 'shoppinglist12345';
    ```
* Create a database instance.
    ```
    CREATE DATABASE shoppinglist owner shoppinglist encoding 'utf-8';
    ```
* Create the test database instance.
    ```
    CREATE DATABASE test_shoppinglist owner shoppinglist encoding 'utf-8';
    ```

## Installation
* Clone this repo into any directory in your machine
* Ensure you have `python 3.5` and `virualenv` installed in your machine
* Create a virtual environment for the project :
    ```
    virtualenv venv
    ```
* Create a .env file at the root of the project folder and add the following
    ```
    source venv/bin/activate
    export db_url='postgresql://shoppinglist:shoppinglist12345@localhost:5432/shopinglist'
    export SECRET_KEY='any-long-string-with-random-characters-you-deem-necessary'
    export FLASK_CONFIG="development"
    export test_db='postgresql://shoppinglist:shoppinglist12345@localhost:5432/test_shopinglist'
    ```
* Run the following to add the above in the environment
    ```
    source .env
    ```
* Install the required packages:
    ```
    pip install -r requirements.txt
    ```
* Run Migrations to setup the database
    ```
    flask db migrate
    flask db upgrade
    ```

## Testing
* Run the following to test rhe application and obtain coverage
    ```
    coverage run --source=. -m py.test && coverage report
    ```

## Launching the Program
* Run the app with the following command
    ```
    python run.py runserver
    ```

## API

```
Spicey stuff about the API, wait for it...
```

## Authors
[Macharia Marigi](https://github.com/machariamarigi)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Various resources on the Internet
