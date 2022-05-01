from flask import request, g, url_for, flash
from flask_appbuilder import SimpleFormView
from markupsafe import Markup

from app import db
from app.forms.forms import QuestionSelfAssessedForm, Question2of5Form, Question1of6Form, Question3to3Form, \
    Question2DecimalsForm, Question1DecimalForm, QuestionSelect4Form
from app.models.general import QuestionType, Question
from app.models.relations import AssocUserQuestion
from app.security.models import ExtendedUser
from app.utils.general import get_question
from app.views.widgets import ExtendedEditWidget


class QuestionSelfAssessedFormView(SimpleFormView):
    form = QuestionSelfAssessedForm
    form_title = 'Selbstkontrolle'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(
            QuestionType.self_assessed.value)

        if question_result == None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id

        answer_value = request.args.get('answer')
        if answer_value:
            is_answer_correct = False

            if answer_value == 'CORRECT':
                user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                    {'correct_questions': ExtendedUser.correct_questions + 1})
                is_answer_correct = True

            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'tried_questions': ExtendedUser.tried_questions + 1})

            # Add entry to answered questions
            answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)
            prev_id = request.args.get('prev_id')
            question_old = db.session.query(Question).filter_by(id=prev_id).first()
            answered_question.question = question_old
            g.user.answered_questions.append(answered_question)

            db.session.commit()

        self.extra_args = {'question': {
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(id=id).first()

        random_url = url_for('QuestionSelfAssessedFormView.this_form_get')
        solution_img = result.solution_image_img()
        correct_link = f'<a class="btn btn-primary" href="{random_url}?answer=CORRECT&prev_id={id}">Richtig</a>'
        incorrect_link = f'<a class="btn btn-primary" href="{random_url}?answer=INCORRECT&prev_id={id}">Falsch</a>'
        description = Markup(f'{solution_img}')
        after_description = Markup(f'{correct_link} {incorrect_link}')

        self.extra_args = {'question': {
            'description': description,
            'after_description': after_description,
            'external_id': result.external_id,
            'submit_text': None},
            'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question2of5FormView(SimpleFormView):
    form = Question2of5Form
    form_title = '2 aus 5'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()

        question_result = get_question(QuestionType.two_of_five.value)
        if question_result == None:
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

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.two_of_five.value).first()
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

        if form.checkbox1.data == result.option1_is_correct:
            form.checkbox1.description = 'Richtig'
        else:
            form.checkbox1.description = 'Falsch'
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = 'Richtig'
        else:
            form.checkbox2.description = 'Falsch'
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = 'Richtig'
        else:
            form.checkbox3.description = 'Falsch'
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = 'Richtig'
        else:
            form.checkbox4.description = 'Falsch'
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = 'Richtig'
        else:
            form.checkbox5.description = 'Falsch'

        if (form.checkbox1.data == result.option1_is_correct) and \
                (form.checkbox2.data == result.option2_is_correct) and \
                (form.checkbox3.data == result.option3_is_correct) and \
                (form.checkbox4.data == result.option4_is_correct) and \
                (form.checkbox5.data == result.option5_is_correct):
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = 'FALSCH!'
            is_answer_correct = False

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)
        answered_question.question = result
        g.user.answered_questions.append(answered_question)

        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question1of6FormView(SimpleFormView):
    form = Question1of6Form
    form_title = '1 aus 6'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.one_of_six.value)
        if question_result == None:
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

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.one_of_six.value).first()
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
        else:
            form.checkbox1.description = 'Falsch'
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = 'Richtig'
        else:
            form.checkbox2.description = 'Falsch'
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = 'Richtig'
        else:
            form.checkbox3.description = 'Falsch'
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = 'Richtig'
        else:
            form.checkbox4.description = 'Falsch'
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = 'Richtig'
        else:
            form.checkbox5.description = 'Falsch'
        if form.checkbox6.data == result.option6_is_correct:
            form.checkbox6.description = 'Richtig'
        else:
            form.checkbox6.description = 'Falsch'

        if (form.checkbox1.data == result.option1_is_correct) and \
                (form.checkbox2.data == result.option2_is_correct) and \
                (form.checkbox3.data == result.option3_is_correct) and \
                (form.checkbox4.data == result.option4_is_correct) and \
                (form.checkbox5.data == result.option5_is_correct) and \
                (form.checkbox6.data == result.option6_is_correct):
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            db.session.commit()
            is_answer_correct = True
        else:
            message = 'FALSCH!'
            is_answer_correct = False

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)
        answered_question.question = result
        g.user.answered_questions.append(answered_question)
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question3to3FormView(SimpleFormView):
    form = Question3to3Form
    form_title = 'Lückentext'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

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
        question_result = get_question(
            QuestionType.three_to_three.value)
        if question_result == None:
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

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.three_to_three.value).first()
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
        else:
            form.checkbox1a.description = 'Falsch'
        if form.checkbox1b.data == result.option1b_is_correct:
            form.checkbox1b.description = 'Richtig'
        else:
            form.checkbox1b.description = 'Falsch'
        if form.checkbox1c.data == result.option1c_is_correct:
            form.checkbox1c.description = 'Richtig'
        else:
            form.checkbox1c.description = 'Falsch'
        if form.checkbox2a.data == result.option2a_is_correct:
            form.checkbox2a.description = 'Richtig'
        else:
            form.checkbox2a.description = 'Falsch'
        if form.checkbox2b.data == result.option2b_is_correct:
            form.checkbox2b.description = 'Richtig'
        else:
            form.checkbox2b.description = 'Falsch'
        if form.checkbox2c.data == result.option2c_is_correct:
            form.checkbox2c.description = 'Richtig'
        else:
            form.checkbox2c.description = 'Falsch'

        if (form.checkbox1a.data == result.option1a_is_correct) and \
                (form.checkbox1b.data == result.option1b_is_correct) and \
                (form.checkbox1c.data == result.option1c_is_correct) and \
                (form.checkbox2a.data == result.option2a_is_correct) and \
                (form.checkbox2b.data == result.option2b_is_correct) and \
                (form.checkbox2c.data == result.option2c_is_correct):
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = 'FALSCH!'
            is_answer_correct = False

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)
        answered_question.question = result
        g.user.answered_questions.append(answered_question)
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question2DecimalsFormView(SimpleFormView):
    form = Question2DecimalsForm
    form_title = 'Werteingabe zwei Zahlen'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.two_decimals.value)
        if question_result == None:
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

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.two_decimals.value).first()
        form.value1.label.text = 'Ergebnis 1'
        form.value2.label.text = 'Ergebnis 2'
        value1_correct = False
        value2_correct = False

        if (form.value1.data <= result.value1_upper_limit) and (form.value1.data >= result.value1_lower_limit):
            form.value1.description = 'Richtig'
            value1_correct = True
        else:
            form.value1.description = 'Falsch'

        if (form.value2.data <= result.value2_upper_limit) and (form.value2.data >= result.value2_lower_limit):
            form.value2.description = 'Richtig'
            value2_correct = True
        else:
            form.value2.description = 'Falsch'

        if value1_correct and value2_correct:
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = f'FALSCH! Richtig gewesen wäre: {result.value1_lower_limit} <= Ergebnis 1 <= {result.value1_upper_limit}, {result.value2_lower_limit} <= Ergebnis 2 <= {result.value2_upper_limit}'
            is_answer_correct = False

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)
        answered_question.question = result
        g.user.answered_questions.append(answered_question)
        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question1DecimalFormView(SimpleFormView):
    form = Question1DecimalForm
    form_title = 'Werteingabe eine Zahl'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.one_decimal.value)
        if question_result == None:
            description = 'Es existieren keine Fragen zu diesem Thema und Typ.'
            external_id = None
            error = True
        else:
            form.id.data = question_result.id
            description = question_result.description_image_img()
            external_id = question_result.external_id
            error = False
            form.value.label.text = 'Ergebnis 1'

        self.extra_args = {'question': {
            'error': error,
            'description': description,
            'external_id': external_id,
            'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.one_decimal.value).first()
        form.value.label.text = 'Ergebnis'
        message = 'FALSCH!'

        if (form.value.data <= result.value1_upper_limit) and (form.value.data >= result.value1_lower_limit):
            form.value.description = 'Richtig'
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = f'FALSCH! Richtig gewesen wäre: {result.value1_lower_limit} <= Ergebnis <= {result.value1_upper_limit}'
            is_answer_correct = False

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)
        answered_question.question = result
        g.user.answered_questions.append(answered_question)

        # TODO: for all commits
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            # TODO: import loggin
            # log.error(c.LOGMSG_ERR_SEC_UPD_USER.format(str(e)))

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class QuestionSelect4FormView(SimpleFormView):
    form = QuestionSelect4Form
    form_title = 'Zuordnung'
    form_template = 'edit_additional.html'
    edit_widget = ExtendedEditWidget

    form_fieldsets = [
        (
            'Antworten',
            {'fields': ['selection1', 'selection2',
                        'selection3', 'selection4']}
        ),
    ]

    def form_get(self, form):
        self.update_redirect()
        question_result = get_question(QuestionType.select_four)
        if question_result == None:
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

        self.extra_args = \
            {'question': {'error': error,
                          'description': description,
                          'options': options,
                          'external_id': external_id,
                          'submit_text': 'Auswerten'}}

    def form_post(self, form):
        self.update_redirect()
        id = form.id.data
        result = db.session.query(Question).filter_by(
            id=id, type=QuestionType.select_four.value).first()
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
        else:
            form.selection1.description = 'Falsch'
        if form.selection2.data == result.selection2_solution.value:
            form.selection2.description = 'Richtig'
        else:
            form.selection2.description = 'Falsch'
        if form.selection3.data == result.selection3_solution.value:
            form.selection3.description = 'Richtig'
        else:
            form.selection3.description = 'Falsch'
        if form.selection4.data == result.selection4_solution.value:
            form.selection4.description = 'Richtig'
        else:
            form.selection4.description = 'Falsch'

        if (form.selection1.data == result.selection1_solution.value) and \
                (form.selection2.data == result.selection2_solution.value) and \
                (form.selection3.data == result.selection3_solution.value) and \
                (form.selection4.data == result.selection4_solution.value):
            message = 'RICHTIG!'
            user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
                {'correct_questions': ExtendedUser.correct_questions + 1})
            is_answer_correct = True
        else:
            message = 'FALSCH!'
            is_answer_correct = False

        user_result = db.session.query(ExtendedUser).filter_by(id=g.user.id).update(
            {'tried_questions': ExtendedUser.tried_questions + 1})

        # Add entry to answered questions
        answered_question = AssocUserQuestion(is_answer_correct=is_answer_correct)
        answered_question.question = result
        g.user.answered_questions.append(answered_question)

        db.session.commit()

        flash(message, 'info')

        self.extra_args = {'question': {'description': result.description_image_img(),
                                        'options': options,
                                        'external_id': result.external_id,
                                        'submit_text': 'Nächste Aufgabe'},
                           'form_action': url_for('QuestionRandom.question_random')}

        # TODO: why necessary? should happen automatically but redirect is wrong?!
        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )