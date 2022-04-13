import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA, IndexView
from flask_migrate import Migrate

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.WARNING)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
migrate = Migrate(app, db)

from .sec import ExtendedSecurityManager  # noqa

# TODO: Should be in views (but circular import)
class ExtendedIndexView(IndexView):
    index_template = 'extended_index.html'


appbuilder = AppBuilder(
    app, db.session, security_manager_class=ExtendedSecurityManager, indexview=ExtendedIndexView)

from . import models, views  # noqa
