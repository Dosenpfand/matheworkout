import calendar

from flask_appbuilder import ModelView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import SimpleFormView
from flask_babel import lazy_gettext as _


from . import appbuilder, db
from .forms import MyForm
from .models import Question2of5


class Question2of5ModelView(ModelView):
    datamodel = SQLAInterface(Question2of5)


class MyFormView(SimpleFormView):
    form = MyForm
    form_title = 'This is my first form view'
    message = 'My form submitted'

    def form_get(self, form):
        form.field1.data = 'This was prefilled'

    def form_post(self, form):
        # post process form
        flash(self.message, 'info')


db.create_all()
appbuilder.add_view(
    Question2of5ModelView,
    "List 2 out of 5 questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    MyFormView,
    "My form View",
    icon="fa-group",
    label=_('My form View'),
    category="My Forms",
    category_icon="fa-cogs")
