"""Module to serve as the entry point to our application"""

# system imports
import os

# local import
from app import create_app


config_name = os.getenv('FLASK_CONFIG')
app = create_app(config_name)

if __name__ == '__main__':
    app.run()
