import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/FlaskApp/")
from app import create_app  # noqa

application = create_app()
