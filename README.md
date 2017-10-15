[![Build Status](https://travis-ci.org/machariamarigi/shopping_list_api.svg)](https://travis-ci.org/machariamarigi/shopping_list_api) [![Coverage Status](https://coveralls.io/repos/github/machariamarigi/shopping_list_api/badge.svg?branch=development)](https://coveralls.io/github/machariamarigi/shopping_list_api?branch=development) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/a4a5c07fde574109bcc1c62ddeddfd20)](https://www.codacy.com/app/machariamarigi/shopping_list_api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=machariamarigi/shopping_list_api&amp;utm_campaign=Badge_Grade) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

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
    python run.py database migrate
    python run.py database upgrade
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

#### Endpoints

| Resource URL                                 |      Methods      |        Description              | Requires Token |
|----------------------------------------------|-------------------|---------------------------------|----------------|
| /api/v1/auth/register                        |POST               |User registers                   |FALSE           |
| /api/v1/auth/login                           |POST               |User login                       |FALSE           |
| /api/v1/auth/reset_password                  |POST               |Reset password for a user        |FALSE           |
| /api/v1/user                                 |GET                |Get details of a user            |TRUE            |
| /api/v1/user                                 |PUT                |Edit a users's details           |TRUE            |
| /api/v1/user                                 |DELETE             |Remove a user from the app       |TRUE            |
| /api/v1/users                                |GET                |List all users                   |TRUE            |
| /api/v1/shoppinglists                        |POST               |Create shopping lists            |TRUE            |
| /api/v1/shoppinglists                        |GET                |List shopping lists              |TRUE            |
| /api/v1/shoppinglist/<list_id>               |GET                |List a single shopping list      |TRUE            |
| /api/v1/shoppinglist/<list_id>               |PUT                |Edit a single shopping list      |TRUE            |
| /api/v1/shoppinglist/<list_id>               |DELETE             |Delete a single shopping list    |TRUE            |
| /api/v1/shoppinglist/<list_id>/items         |POST               |Create items in a shopping list  |TRUE            |
| /api/v1/shoppinglist/<list_id>/items         |GET                |List items in a shopping list    |TRUE            |
| /api/v1/shoppinglist/<list_id>/item/<item_id>|GET                |List an item in a shopping list  |TRUE            |
| /api/v1/shoppinglist/<list_id>/item/<item_id>|PUT                |Edit an item in a shopping list  |TRUE            |
| /api/v1/shoppinglist/<list_id>/item/<item_id>|PATCH              |Buy an item in a shopping list   |TRUE            |
| /api/v1/shoppinglist/<list_id>/item/<item_id>|DELETE             |Delete an item in a shopping list|TRUE            |


## Authors
[Macharia Marigi](https://github.com/machariamarigi)

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments
* Various resources on the Internet
