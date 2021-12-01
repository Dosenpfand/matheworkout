import calendar

from flask_appbuilder import ModelView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import SimpleFormView
from flask_babel import lazy_gettext as _
from flask import flash

from random import randrange


from . import appbuilder, db
from .forms import Question2of5Form
from .models import Question2of5


class Question2of5ModelView(ModelView):
    datamodel = SQLAInterface(Question2of5)


class Question2of5FormView(SimpleFormView):
    form = Question2of5Form
    form_title = '2 of 5 Test'

    def form_get(self, form):
        count = db.session.query(Question2of5).count()
        id = randrange(1, count + 1)
        result = db.session.query(Question2of5).filter_by(id=id).first()

        form.checkbox1.label.text = result.option_correct1
        form.checkbox2.label.text = result.option_correct2
        form.checkbox3.label.text = result.option_incorrect1
        form.checkbox4.label.text = result.option_incorrect2
        form.checkbox5.label.text = result.option_incorrect3

    def form_post(self, form):
        result = db.session.query(Question2of5).filter_by(id=1).first()
        message = str(result.description)
        flash(message, 'info')


db.create_all()
appbuilder.add_view(
    Question2of5ModelView,
    "List 2 out of 5 questions",
    icon="fa-question-circle",
    category="Questions",
    category_icon="fa-question",
)
appbuilder.add_view(
    Question2of5FormView,
    "2 of 5 Test",
    icon="fa-group",
    label=_("2 of 5 Test"),
    category="Tests",
    category_icon="fa-cogs")
