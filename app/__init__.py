import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA, IndexView

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.WARNING)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)

from .sec import ExtendedSecurityManager  # noqa

# TODO: Should be in views (but circular import)
class ExtendedIndexView(IndexView):
    index_template = 'extended_index.html'


appbuilder = AppBuilder(
    app, db.session, security_manager_class=ExtendedSecurityManager, indexview=ExtendedIndexView)

from . import models, views  # noqa
