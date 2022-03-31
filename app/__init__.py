import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_appbuilder.menu import Menu


logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)

from .sec import ExtendedSecurityManager # noqa

appbuilder = AppBuilder(app, db.session, security_manager_class=ExtendedSecurityManager)

from . import models, views  # noqa
