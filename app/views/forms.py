from flask import request, g, url_for, flash
from flask_appbuilder import SimpleFormView, expose, has_access
from markupsafe import Markup

from app import db
from app.forms.forms import QuestionSelfAssessedForm, Question2of5Form, Question1of6Form, Question3to3Form, \
    Question2DecimalsForm, Question1DecimalForm, QuestionSelect4Form
from app.models.general import QuestionType, Question, Assignment
from app.models.relations import AssocUserQuestion
from app.security.models import ExtendedUser
from app.utils.general import get_question, commit_safely
from app.views.widgets import ExtendedEditWidget


# TODO: expand base class? also in models.py?
class QuestionFormView(SimpleFormView):
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def __init__(self):
        super().__init__()
        self.assignment_id = None
        self.ext_id = None

    @expose("/form")
    @expose("/form/<int:ext_id>")
    @expose("/form/<int:ext_id>/<int:assignment_id>")
    @has_access
    def this_form_get(self, ext_id=None, assignment_id=None):
        self.ext_id = ext_id
        self.assignment_id = assignment_id
        return super().this_form_get()

    @expose("/form", methods=["POST"])
    @expose("/form/<int:ext_id>", methods=["POST"])
    @expose("/form/<int:ext_id>/<int:assignment_id>", methods=["POST"])
    @has_access
    def this_form_post(self, ext_id=None, assignment_id=None):
        return super().this_form_post()

    def get_forward_button(self, question_id):
        forward_text = None
        forward_url = None
        if self.assignment_id:
            assignment = db.session.query(Assignment).filter_by(id=self.assignment_id).first()
            take_next = False
            next_ext_id = None
            # TODO: optimize
            for assigned_question in assignment.assigned_questions:
                if take_next:
                    next_ext_id = assigned_question.external_id
                    break
                if assigned_question.id == question_id:
                    take_next = True

            if next_ext_id:
                forward_text = 'Nächste Aufgabe'
                forward_url = url_for('ExtIdToForm.ext_id_to_form', ext_id=next_ext_id,
                                      assignment_id=self.assignment_id)
            else:
                forward_text = 'Zur Übungsübersicht'
                forward_url = url_for('AssignmentModelStudentView.show', pk=self.assignment_id)
        return forward_text, forward_url

    def get_assignment_progress(self, question_id):
        assignment_progress = None
        if self.assignment_id:
            assignment = db.session.query(Assignment).filter_by(id=self.assignment_id).first()
            # TODO: optimize
            for i, assigned_question in enumerate(assignment.assigned_questions, 1):
                if assigned_question.id == question_id:
                    break

            assignment_progress = {'done': i, 'total': len(assignment.assigned_questions),
                                   'percentage': round(i / len(assignment.assigned_questions) * 100)}
        return assignment_progress


class QuestionSelfAssessedFormView(QuestionFormView):
    form = QuestionSelfAssessedForm
    form_title = 'Selbstkontrolle'

    # TODO: html input id, csrf, etc. are twice in output!
    def form_get(self, form):
        question_result = get_question(QuestionType.self_assessed.value, self.ext_id)

        if question_result is None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id

            assignment_progress = self.get_assignment_progress(question_result.id)

            answer_value = request.args.get('answer')
            if answer_value:
                is_answer_correct = False

                if answer_value == 'CORRECT':
                    db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                        {'correct_questions': ExtendedUser.correct_questions + 1})
                    is_answer_correct = True

                db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                    {'tried_questions': ExtendedUser.tried_questions + 1})

                # Add entry to answered questions
                answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)  # noqa
                answered_question.question = question_result
                g.user.answered_questions.append(answered_question)
                commit_safely(db.session)

                forward_text, forward_url = self.get_forward_button(question_result.id)
                submit_text = None
                back_count = 2
            else:
                forward_text, forward_url = None, None
                submit_text = 'Auswerten'
                back_count = 1
                self.update_redirect()

        self.extra_args = {'question': {
            'description': description,
            'external_id': external_id,
            'submit_text': submit_text,
            'back_count': back_count,
            'forward_text': forward_text,
            'forward_url': forward_url,
            'assignment_progress': assignment_progress}}

    def form_post(self, form):
        question_id = int(form.id.data)
        result = db.session.query(Question).filter_by(id=question_id).first()

        url = url_for('QuestionSelfAssessedFormView.this_form_get', ext_id=result.external_id,
                      assignment_id=self.assignment_id)

        solution_img = result.solution_image_img()
        correct_link = \
            f'<a class="btn btn-primary" href="{url}?answer=CORRECT">Richtig</a>'
        incorrect_link = \
            f'<a class="btn btn-primary" href="{url}?answer=INCORRECT">Falsch</a>'
        description = Markup(f'{solution_img}')
        after_description = Markup(f'{correct_link} {incorrect_link}')

        assignment_progress = self.get_assignment_progress(question_id)

        self.extra_args = {'question': {
            'description': description,
            'after_description': after_description,
            'external_id': result.external_id,
            'submit_text': None,
            'video_embed_url': result.video_embed_url(),
            'assignment_progress': assignment_progress}}

        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question2of5FormView(QuestionFormView):
    form = Question2of5Form
    form_title = '2 aus 5'

    def form_get(self, form):
        self.update_redirect()

        question_result = get_question(QuestionType.two_of_five.value, self.ext_id)
        if question_result is None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False

            form.checkbox1.label.text = question_result.get_option_image(
                question_result.option1_image)
            form.checkbox2.label.text = question_result.get_option_image(
                question_result.option2_image)
            form.checkbox3.label.text = question_result.get_option_image(
                question_result.option3_image)
            form.checkbox4.label.text = question_result.get_option_image(
                question_result.option4_image)
            form.checkbox5.label.text = question_result.get_option_image(
                question_result.option5_image)

            assignment_progress = self.get_assignment_progress(question_result.id)

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten',
            'assignment_progress': assignment_progress}}

    def form_post(self, form):
        self.update_redirect()
        question_id = int(form.id.data)
        result = db.session.query(Question).filter_by(
            id=question_id, type=QuestionType.two_of_five.value).first()
        form.checkbox1.label.text = result.get_option_image(result.option1_image)
        form.checkbox2.label.text = result.get_option_image(result.option2_image)
        form.checkbox3.label.text = result.get_option_image(result.option3_image)
        form.checkbox4.label.text = result.get_option_image(result.option4_image)
        form.checkbox5.label.text = result.get_option_image(result.option5_image)

        if form.checkbox1.data == result.option1_is_correct:
            form.checkbox1.description = 'Richtig'
            form.checkbox1.render_kw = {'row_class': 'success'}
        else:
            form.checkbox1.description = 'Falsch'
            form.checkbox1.render_kw = {'row_class': 'danger'}
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = 'Richtig'
            form.checkbox2.render_kw = {'row_class': 'success'}
        else:
            form.checkbox2.description = 'Falsch'
            form.checkbox2.render_kw = {'row_class': 'danger'}
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = 'Richtig'
            form.checkbox3.render_kw = {'row_class': 'success'}
        else:
            form.checkbox3.description = 'Falsch'
            form.checkbox3.render_kw = {'row_class': 'danger'}
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = 'Richtig'
            form.checkbox4.render_kw = {'row_class': 'success'}
        else:
            form.checkbox4.description = 'Falsch'
            form.checkbox4.render_kw = {'row_class': 'danger'}
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = 'Richtig'
            form.checkbox5.render_kw = {'row_class': 'success'}
        else:
            form.checkbox5.description = 'Falsch'
            form.checkbox5.render_kw = {'row_class': 'danger'}

        if (form.checkbox1.data == result.option1_is_correct) and \
                (form.checkbox2.data == result.option2_is_correct) and \
                (form.checkbox3.data == result.option3_is_correct) and \
                (form.checkbox4.data == result.option4_is_correct) and \
                (form.checkbox5.data == result.option5_is_correct):
            message = 'RICHTIG!'
            category = 'success'
            db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = 'FALSCH!'
            category = 'danger'
            is_answer_correct = False

        db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)  # noqa
        answered_question.question = result
        g.user.answered_questions.append(answered_question)
        commit_safely(db.session)

        flash(message, category)

        # TODO: does not work when post is re-sent!
        forward_text, forward_url = self.get_forward_button(question_id)
        assignment_progress = self.get_assignment_progress(question_id)

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'video_embed_url': result.video_embed_url(),
                                        'forward_text': forward_text,
                                        'forward_url': forward_url,
                                        'assignment_progress': assignment_progress}}

        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question1of6FormView(QuestionFormView):
    form = Question1of6Form
    form_title = '1 aus 6'

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.one_of_six.value, self.ext_id)

        if question_result is None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False

            form.checkbox1.label.text = question_result.get_option_image(
                question_result.option1_image)
            form.checkbox2.label.text = question_result.get_option_image(
                question_result.option2_image)
            form.checkbox3.label.text = question_result.get_option_image(
                question_result.option3_image)
            form.checkbox4.label.text = question_result.get_option_image(
                question_result.option4_image)
            form.checkbox5.label.text = question_result.get_option_image(
                question_result.option5_image)
            form.checkbox6.label.text = question_result.get_option_image(
                question_result.option6_image)

            assignment_progress = self.get_assignment_progress(question_result.id)

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten',
            'assignment_progress': assignment_progress}}

    def form_post(self, form):
        self.update_redirect()
        question_id = int(form.id.data)
        result = db.session.query(Question).filter_by(
            id=question_id, type=QuestionType.one_of_six.value).first()
        form.checkbox1.label.text = result.get_option_image(
            result.option1_image)
        form.checkbox2.label.text = result.get_option_image(
            result.option2_image)
        form.checkbox3.label.text = result.get_option_image(
            result.option3_image)
        form.checkbox4.label.text = result.get_option_image(
            result.option4_image)
        form.checkbox5.label.text = result.get_option_image(
            result.option5_image)
        form.checkbox6.label.text = result.get_option_image(
            result.option6_image)

        if form.checkbox1.data == result.option1_is_correct:
            form.checkbox1.description = 'Richtig'
            form.checkbox1.render_kw = {'row_class': 'success'}
        else:
            form.checkbox1.description = 'Falsch'
            form.checkbox1.render_kw = {'row_class': 'danger'}
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = 'Richtig'
            form.checkbox2.render_kw = {'row_class': 'success'}
        else:
            form.checkbox2.description = 'Falsch'
            form.checkbox2.render_kw = {'row_class': 'danger'}
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = 'Richtig'
            form.checkbox3.render_kw = {'row_class': 'success'}
        else:
            form.checkbox3.description = 'Falsch'
            form.checkbox3.render_kw = {'row_class': 'danger'}
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = 'Richtig'
            form.checkbox4.render_kw = {'row_class': 'success'}
        else:
            form.checkbox4.description = 'Falsch'
            form.checkbox4.render_kw = {'row_class': 'danger'}
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = 'Richtig'
            form.checkbox5.render_kw = {'row_class': 'success'}
        else:
            form.checkbox5.description = 'Falsch'
            form.checkbox5.render_kw = {'row_class': 'danger'}
        if form.checkbox6.data == result.option6_is_correct:
            form.checkbox6.description = 'Richtig'
            form.checkbox6.render_kw = {'row_class': 'success'}
        else:
            form.checkbox6.description = 'Falsch'
            form.checkbox6.render_kw = {'row_class': 'danger'}

        if (form.checkbox1.data == result.option1_is_correct) and \
                (form.checkbox2.data == result.option2_is_correct) and \
                (form.checkbox3.data == result.option3_is_correct) and \
                (form.checkbox4.data == result.option4_is_correct) and \
                (form.checkbox5.data == result.option5_is_correct) and \
                (form.checkbox6.data == result.option6_is_correct):
            message = 'RICHTIG!'
            category = 'success'
            db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            commit_safely(db.session)
            is_answer_correct = True
        else:
            message = 'FALSCH!'
            category = 'danger'
            is_answer_correct = False

        db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)  # noqa
        answered_question.question = result
        g.user.answered_questions.append(answered_question)
        commit_safely(db.session)

        flash(message, category)

        forward_text, forward_url = self.get_forward_button(question_id)
        assignment_progress = self.get_assignment_progress(question_id)

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'video_embed_url': result.video_embed_url(),
                                        'forward_text': forward_text,
                                        'forward_url': forward_url,
                                        'assignment_progress': assignment_progress}}

        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question3to3FormView(QuestionFormView):
    form = Question3to3Form
    form_title = 'Lückentext'

    form_fieldsets = [
        (
            '1',
            {'fields': ['checkbox1a', 'checkbox1b', 'checkbox1c']}
        ),
        (
            '2',
            {'fields': ['checkbox2a', 'checkbox2b', 'checkbox2c']}
        ),
    ]

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.three_to_three.value, self.ext_id)

        if question_result is None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False

            form.checkbox1a.label.text = question_result.get_option_small_image(
                question_result.option1a_image)
            form.checkbox1b.label.text = question_result.get_option_small_image(
                question_result.option1b_image)
            form.checkbox1c.label.text = question_result.get_option_small_image(
                question_result.option1c_image)
            form.checkbox2a.label.text = question_result.get_option_small_image(
                question_result.option2a_image)
            form.checkbox2b.label.text = question_result.get_option_small_image(
                question_result.option2b_image)
            form.checkbox2c.label.text = question_result.get_option_small_image(
                question_result.option2c_image)

            assignment_progress = self.get_assignment_progress(question_result.id)

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten',
            'assignment_progress': assignment_progress}}

    def form_post(self, form):
        self.update_redirect()
        question_id = int(form.id.data)
        result = db.session.query(Question).filter_by(
            id=question_id, type=QuestionType.three_to_three.value).first()
        form.checkbox1a.label.text = result.get_option_small_image(
            result.option1a_image)
        form.checkbox1b.label.text = result.get_option_small_image(
            result.option1b_image)
        form.checkbox1c.label.text = result.get_option_small_image(
            result.option1c_image)
        form.checkbox2a.label.text = result.get_option_small_image(
            result.option2a_image)
        form.checkbox2b.label.text = result.get_option_small_image(
            result.option2b_image)
        form.checkbox2c.label.text = result.get_option_small_image(
            result.option2c_image)

        if form.checkbox1a.data == result.option1a_is_correct:
            form.checkbox1a.description = 'Richtig'
            form.checkbox1a.render_kw = {'row_class': 'success'}
        else:
            form.checkbox1a.description = 'Falsch'
            form.checkbox1a.render_kw = {'row_class': 'danger'}
        if form.checkbox1b.data == result.option1b_is_correct:
            form.checkbox1b.description = 'Richtig'
            form.checkbox1b.render_kw = {'row_class': 'success'}
        else:
            form.checkbox1b.description = 'Falsch'
            form.checkbox1c.render_kw = {'row_class': 'danger'}
        if form.checkbox1c.data == result.option1c_is_correct:
            form.checkbox1c.description = 'Richtig'
            form.checkbox1c.render_kw = {'row_class': 'success'}
        else:
            form.checkbox1c.description = 'Falsch'
            form.checkbox1c.render_kw = {'row_class': 'danger'}
        if form.checkbox2a.data == result.option2a_is_correct:
            form.checkbox2a.description = 'Richtig'
            form.checkbox2a.render_kw = {'row_class': 'success'}
        else:
            form.checkbox2a.description = 'Falsch'
            form.checkbox2a.render_kw = {'row_class': 'danger'}
        if form.checkbox2b.data == result.option2b_is_correct:
            form.checkbox2b.description = 'Richtig'
            form.checkbox2b.render_kw = {'row_class': 'success'}
        else:
            form.checkbox2b.description = 'Falsch'
            form.checkbox2b.render_kw = {'row_class': 'danger'}
        if form.checkbox2c.data == result.option2c_is_correct:
            form.checkbox2c.description = 'Richtig'
            form.checkbox2c.render_kw = {'row_class': 'success'}
        else:
            form.checkbox2c.description = 'Falsch'
            form.checkbox2c.render_kw = {'row_class': 'danger'}

        if (form.checkbox1a.data == result.option1a_is_correct) and \
                (form.checkbox1b.data == result.option1b_is_correct) and \
                (form.checkbox1c.data == result.option1c_is_correct) and \
                (form.checkbox2a.data == result.option2a_is_correct) and \
                (form.checkbox2b.data == result.option2b_is_correct) and \
                (form.checkbox2c.data == result.option2c_is_correct):
            message = 'RICHTIG!'
            category = 'success'
            db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = 'FALSCH!'
            category = 'danger'
            is_answer_correct = False

        db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)  # noqa
        answered_question.question = result
        g.user.answered_questions.append(answered_question)
        commit_safely(db.session)

        flash(message, category)

        forward_text, forward_url = self.get_forward_button(question_id)
        assignment_progress = self.get_assignment_progress(question_id)

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'video_embed_url': result.video_embed_url(),
                                        'forward_text': forward_text,
                                        'forward_url': forward_url,
                                        'assignment_progress': assignment_progress}}

        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question2DecimalsFormView(QuestionFormView):
    form = Question2DecimalsForm
    form_title = 'Werteingabe zwei Zahlen'

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.two_decimals.value, self.ext_id)

        if question_result is None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False

            form.value1.label.text = 'Ergebnis 1'
            form.value2.label.text = 'Ergebnis 2'

            assignment_progress = self.get_assignment_progress(question_result.id)

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten',
            'assignment_progress': assignment_progress}}

    def form_post(self, form):
        self.update_redirect()
        question_id = int(form.id.data)
        result = db.session.query(Question).filter_by(
            id=question_id, type=QuestionType.two_decimals.value).first()
        form.value1.label.text = 'Ergebnis 1'
        form.value2.label.text = 'Ergebnis 2'
        value1_correct = False
        value2_correct = False

        if (form.value1.data <= result.value1_upper_limit) and (form.value1.data >= result.value1_lower_limit):
            form.value1.description = 'Richtig'
            form.value1.render_kw = {'row_class': 'success'}
            value1_correct = True
        else:
            form.value1.description = 'Falsch'
            form.value1.render_kw = {'row_class': 'danger'}

        if (form.value2.data <= result.value2_upper_limit) and (form.value2.data >= result.value2_lower_limit):
            form.value2.description = 'Richtig'
            form.value2.render_kw = {'row_class': 'success'}
            value2_correct = True
        else:
            form.value2.description = 'Falsch'
            form.value2.render_kw = {'row_class': 'danger'}

        if value1_correct and value2_correct:
            message = 'RICHTIG!'
            category = 'success'
            db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = \
                f'FALSCH! Richtig gewesen wäre: ' \
                f'{result.value1_lower_limit} <= Ergebnis 1 <= {result.value1_upper_limit},' \
                f'{result.value2_lower_limit} <= Ergebnis 2 <= {result.value2_upper_limit}'
            category = 'danger'
            is_answer_correct = False

        db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)  # noqa
        answered_question.question = result
        g.user.answered_questions.append(answered_question)
        commit_safely(db.session)

        flash(message, category)

        forward_text, forward_url = self.get_forward_button(question_id)
        assignment_progress = self.get_assignment_progress(question_id)

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'video_embed_url': result.video_embed_url(),
                                        'forward_text': forward_text,
                                        'forward_url': forward_url,
                                        'assignment_progress': assignment_progress}}

        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question1DecimalFormView(QuestionFormView):
    form = Question1DecimalForm
    form_title = 'Werteingabe eine Zahl'

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.one_decimal.value, self.ext_id)

        if question_result is None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False
            form.value.label.text = 'Ergebnis 1'

            assignment_progress = self.get_assignment_progress(question_result.id)

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten',
            'assignment_progress': assignment_progress}}

    def form_post(self, form):
        self.update_redirect()
        question_id = int(form.id.data)
        result = db.session.query(Question).filter_by(
            id=question_id, type=QuestionType.one_decimal.value).first()
        form.value.label.text = 'Ergebnis'

        if (form.value.data <= result.value1_upper_limit) and (form.value.data >= result.value1_lower_limit):
            form.value.description = 'Richtig'
            message = 'RICHTIG!'
            category = 'success'
            db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = \
                f'FALSCH! Richtig gewesen wäre: {result.value1_lower_limit} <= Ergebnis <= {result.value1_upper_limit}'
            category = 'danger'
            is_answer_correct = False

        db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)  # noqa
        answered_question.question = result
        g.user.answered_questions.append(answered_question)
        commit_safely(db.session)

        flash(message, category)

        forward_text, forward_url = self.get_forward_button(question_id)
        assignment_progress = self.get_assignment_progress(question_id)

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'video_embed_url': result.video_embed_url(),
                                        'forward_text': forward_text,
                                        'forward_url': forward_url,
                                        'assignment_progress': assignment_progress}}

        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class QuestionSelect4FormView(QuestionFormView):
    form = QuestionSelect4Form
    form_title = 'Zuordnung'

    form_fieldsets = [
        (
            'Antworten',
            {'fields': ['selection1', 'selection2',
                        'selection3', 'selection4']}
        ),
    ]

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.select_four.value, self.ext_id)

        if question_result is None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            options = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            options = {'A': question_result.get_option_small_image(question_result.option1_image),
                       'B': question_result.get_option_small_image(question_result.option2_image),
                       'C': question_result.get_option_small_image(question_result.option3_image),
                       'D': question_result.get_option_small_image(question_result.option4_image),
                       'E': question_result.get_option_small_image(question_result.option5_image),
                       'F': question_result.get_option_small_image(question_result.option6_image)}
            error = False

            form.selection1.label.text = question_result.get_selection_image(
                question_result.selection1_image)
            form.selection2.label.text = question_result.get_selection_image(
                question_result.selection2_image)
            form.selection3.label.text = question_result.get_selection_image(
                question_result.selection3_image)
            form.selection4.label.text = question_result.get_selection_image(
                question_result.selection4_image)

            assignment_progress = self.get_assignment_progress(question_result.id)

        self.extra_args = \
            {'question': {'error': error,
                          'description': description,
                          'options': options,
                          'external_id': external_id,
                          'submit_text': 'Auswerten',
                          'assignment_progress': assignment_progress}}

    def form_post(self, form):
        self.update_redirect()
        question_id = int(form.id.data)
        result = db.session.query(Question).filter_by(
            id=question_id, type=QuestionType.select_four.value).first()
        form.selection1.label.text = result.get_selection_image(
            result.selection1_image)
        form.selection2.label.text = result.get_selection_image(
            result.selection2_image)
        form.selection3.label.text = result.get_selection_image(
            result.selection3_image)
        form.selection4.label.text = result.get_selection_image(
            result.selection4_image)
        options = {'A': result.get_option_small_image(result.option1_image),
                   'B': result.get_option_small_image(result.option2_image),
                   'C': result.get_option_small_image(result.option3_image),
                   'D': result.get_option_small_image(result.option4_image),
                   'E': result.get_option_small_image(result.option5_image),
                   'F': result.get_option_small_image(result.option6_image)}

        if form.selection1.data == result.selection1_solution.value:
            form.selection1.description = 'Richtig'
            form.selection1.render_kw = {'row_class': 'success'}
        else:
            form.selection1.description = 'Falsch'
            form.selection1.render_kw = {'row_class': 'danger'}
        if form.selection2.data == result.selection2_solution.value:
            form.selection2.description = 'Richtig'
            form.selection2.render_kw = {'row_class': 'success'}
        else:
            form.selection2.description = 'Falsch'
            form.selection2.render_kw = {'row_class': 'danger'}
        if form.selection3.data == result.selection3_solution.value:
            form.selection3.description = 'Richtig'
            form.selection3.render_kw = {'row_class': 'success'}
        else:
            form.selection3.description = 'Falsch'
            form.selection3.render_kw = {'row_class': 'danger'}
        if form.selection4.data == result.selection4_solution.value:
            form.selection4.description = 'Richtig'
            form.selection4.render_kw = {'row_class': 'success'}
        else:
            form.selection4.description = 'Falsch'
            form.selection4.render_kw = {'row_class': 'danger'}

        if (form.selection1.data == result.selection1_solution.value) and \
                (form.selection2.data == result.selection2_solution.value) and \
                (form.selection3.data == result.selection3_solution.value) and \
                (form.selection4.data == result.selection4_solution.value):
            message = 'RICHTIG!'
            category = 'success'
            db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = 'FALSCH!'
            category = 'danger'
            is_answer_correct = False

        db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)  # noqa
        answered_question.question = result
        g.user.answered_questions.append(answered_question)

        commit_safely(db.session)

        flash(message, category)

        forward_text, forward_url = self.get_forward_button(question_id)
        assignment_progress = self.get_assignment_progress(question_id)

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'options': options,
                                        'external_id': result.external_id,
                                        'video_embed_url': result.video_embed_url(),
                                        'forward_text': forward_text,
                                        'forward_url': forward_url,
                                        'assignment_progress': assignment_progress}}

        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )
