"""Module to serve as the entry point to our application"""

# system imports
import os

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

# local import
from app import create_app
from models import db


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)
manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('database', MigrateCommand)

if __name__ == '__main__':
    manager.run()
