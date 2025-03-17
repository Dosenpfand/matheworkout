import logging
import sys

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/FlaskApp/")
from app import create_app  # noqa

app = create_app()
