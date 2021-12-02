from random import randrange
from flask_appbuilder import ModelView, BaseView, SimpleFormView, expose, has_access
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import lazy_gettext as _
from flask import render_template, flash, redirect, url_for
from . import appbuilder, db
from .forms import Question2of5Form
from .models import Question2of5


class Question2of5ModelView(ModelView):
    datamodel = SQLAInterface(Question2of5)


class Question2of5FormView(SimpleFormView):
    form = Question2of5Form
    form_title = '2 of 5 Test'
    form_template = 'edit_additional.html'

    def form_get(self, form):
        self.update_redirect()
        # Get random question
        # TODO: no gaps in ID allowed!
        count = db.session.query(Question2of5).count()
        id = randrange(1, count + 1)
        result = db.session.query(Question2of5).filter_by(id=id).first()

        form.id.data = id
        form.checkbox1.label.text = result.option1_description
        form.checkbox2.label.text = result.option2_description
        form.checkbox3.label.text = result.option3_description
        form.checkbox4.label.text = result.option4_description
        form.checkbox5.label.text = result.option5_description

        self.extra_args = {'question': {'title': result.title,
                                        'description': result.description}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question2of5).filter_by(id=id).first()
        form.checkbox1.label.text = result.option1_description
        form.checkbox2.label.text = result.option2_description
        form.checkbox3.label.text = result.option3_description
        form.checkbox4.label.text = result.option4_description
        form.checkbox5.label.text = result.option5_description

        if form.checkbox1.data == result.option1_is_correct:
            form.checkbox1.description = 'correct'
        else:
            form.checkbox1.description = 'incorrect'
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = 'correct'
        else:
            form.checkbox2.description = 'incorrect'
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = 'correct'
        else:
            form.checkbox3.description = 'incorrect'
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = 'correct'
        else:
            form.checkbox4.description = 'incorrect'
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = 'correct'
        else:
            form.checkbox5.description = 'incorrect'

        if (form.checkbox1.data == result.option1_is_correct) and \
            (form.checkbox2.data == result.option2_is_correct) and \
                (form.checkbox3.data == result.option3_is_correct) and \
            (form.checkbox4.data == result.option4_is_correct) and \
                (form.checkbox5.data == result.option5_is_correct):
            message = 'CORRECT!'
        else:
            message = 'INCORRECT!'
        flash(message, 'info')

        self.extra_args = {'question': {'title': result.title,
                                        'description': result.description}}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
                    self.form_template,
                    title=self.form_title,
                    widgets=widgets,
                    appbuilder=self.appbuilder,
                )
        # return redirect(url_for('Question2of5EvaluateView.evaluate'))  # , id=DBTable.id))
        # result = db.session.query(Question2of5).filter_by(id=1).first()


class Question2of5EvaluateView(BaseView):
    route_base = "/question2of5evaluateview"
    default_view = "evaluate"

    @ expose('/evaluate')
    @ has_access
    def evaluate(self):
        param1 = 'Goodbye'
        self.update_redirect()
        return self.render_template('method3.html', param1=param1)


appbuilder.add_view(Question2of5EvaluateView(),
                    "Evaluate", category="Evaluate")

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
