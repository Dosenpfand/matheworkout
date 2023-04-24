import sys
import logging

logging.basicConfig(stream=sys.stderr)

from app import create_app  # noqa

app = create_app()
