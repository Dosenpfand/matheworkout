import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA, IndexView
from flask_appbuilder.menu import Menu

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)

from .sec import ExtendedSecurityManager  # noqa

# Should be in views (but circular import)
class ExtendedIndexView(IndexView):
    index_template = 'extended_index.html'

appbuilder = AppBuilder(
    app, db.session, security_manager_class=ExtendedSecurityManager, indexview=ExtendedIndexView)

from . import models, views  # noqa
