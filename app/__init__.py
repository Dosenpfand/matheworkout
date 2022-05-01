import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
from flask_migrate import Migrate

from app.views.index import ExtendedIndexView

logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.WARNING)

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
migrate = Migrate(app, db)

from app.security.general import ExtendedSecurityManager  # noqa

appbuilder = AppBuilder(
    app, db.session, security_manager_class=ExtendedSecurityManager, indexview=ExtendedIndexView,
    base_template='extended_base.html')

from app.models import general # noqa
from app.views import views # noqa
