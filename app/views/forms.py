import datetime

from flask import (
    request,
    g,
    url_for,
    flash,
    current_app,
    redirect,
    abort,
    make_response,
    jsonify,
    session,
)
from flask_appbuilder import SimpleFormView, expose, has_access
from flask_appbuilder.models.sqla.interface import SQLAInterface
from markupsafe import Markup
from sqlalchemy import asc

from app import db, appbuilder
from app.forms.forms import (
    QuestionSelfAssessedForm,
    Question2of5Form,
    Question1of6Form,
    Question3to3Form,
    Question2DecimalsForm,
    Question1DecimalForm,
    QuestionSelect4Form,
    DeleteStatsForm,
    ImportUsersForm,
    AddQuestionToAssignmentForm,
    DeleteAccountForm,
)
from app.models.general import (
    Achievement,
    QuestionType,
    Question,
    Assignment,
    AssocUserQuestion,
    assoc_assignment_question,
)
from app.utils.general import commit_safely, send_email
from app.views.achievements import check_for_new_achievement
from app.views.widgets import ExtendedEditWidget, FormMinimalInlineWidget


class QuestionFormView(SimpleFormView):
    form_template = "edit_additional.html"
    edit_widget = ExtendedEditWidget

    def __init__(self):
        super().__init__()
        self.id = None
        self.is_random = None
        self.assignment_id = None
        self.category_id = None
        self.topic_id = None

    @expose("/form")
    @expose("/form/<int:q_id>")
    @expose("/form/<int:q_id>/random/<int:is_random>")
    @expose("/form/<int:q_id>/assignment/<int:assignment_id>")
    @expose("/form/<int:q_id>/category/<int:category_id>")
    @expose("/form/<int:q_id>/topic/<int:topic_id>")
    @expose("/form/<int:q_id>/topic/<int:topic_id>/random/<int:is_random>")
    @has_access
    def this_form_get(
        self,
        q_id=None,
        is_random=None,
        assignment_id=None,
        category_id=None,
        topic_id=None,
    ):
        self.id = q_id
        self.is_random = is_random
        self.assignment_id = assignment_id
        self.category_id = category_id
        self.topic_id = topic_id
        return super().this_form_get()

    @expose("/form", methods=["POST"])
    @expose("/form/<int:q_id>", methods=["POST"])
    @expose("/form/<int:q_id>/random/<int:is_random>", methods=["POST"])
    @expose("/form/<int:q_id>/assignment/<int:assignment_id>", methods=["POST"])
    @expose("/form/<int:q_id>/category/<int:category_id>", methods=["POST"])
    @expose("/form/<int:q_id>/topic/<int:topic_id>", methods=["POST"])
    @expose(
        "/form/<int:q_id>/topic/<int:topic_id>/random/<int:is_random>", methods=["POST"]
    )
    @has_access
    def this_form_post(
        self,
        q_id=None,
        is_random=None,
        assignment_id=None,
        category_id=None,
        topic_id=None,
    ):
        self.id = q_id
        self.is_random = is_random
        self.assignment_id = assignment_id
        self.category_id = category_id
        self.topic_id = topic_id
        return super().this_form_post()

    def get_forward_button(self, question_id):
        forward_text = None
        forward_url = None

        if self.is_random:
            forward_text = "Nächste Zufallsaufgabe"
            forward_url = url_for(
                "QuestionRandom.random_question_redirect", topic_id=self.topic_id
            )
        elif self.assignment_id:
            questions = (
                db.session.query(Question)
                .join(assoc_assignment_question)
                .join(Assignment)
                .filter(Assignment.id == self.assignment_id)
                .order_by(asc(Question.external_id))
            )
            take_next = False
            next_id = None
            for assigned_question in questions:
                if take_next:
                    next_id = assigned_question.id
                    break
                if assigned_question.id == question_id:
                    take_next = True

            if next_id:
                forward_text = "Nächste Aufgabe"
                forward_url = url_for(
                    "IdToForm.id_to_form",
                    q_id=next_id,
                    assignment_id=self.assignment_id,
                )
            else:
                forward_text = "Zur Übungsübersicht"
                forward_url = url_for(
                    "AssignmentModelStudentView.show", pk=self.assignment_id
                )
        elif self.category_id or self.topic_id:
            if self.category_id:
                questions = (
                    db.session.query(Question)
                    .filter_by(category_id=self.category_id)
                    .order_by(asc(Question.external_id))
                )
            else:
                questions = (
                    db.session.query(Question)
                    .filter_by(topic_id=self.topic_id)
                    .order_by(asc(Question.external_id))
                )
            take_next = False
            next_id = None
            for question in questions:
                if take_next:
                    next_id = question.id
                    break
                if question.id == question_id:
                    take_next = True

            if next_id:
                forward_text = "Nächste Aufgabe"
                if self.category_id:
                    forward_url = url_for(
                        "IdToForm.id_to_form",
                        q_id=next_id,
                        category_id=self.category_id,
                    )
                else:
                    forward_url = url_for(
                        "IdToForm.id_to_form", q_id=next_id, topic_id=self.topic_id
                    )
            else:
                forward_text = "Zur Übungsübersicht"
                if self.category_id:
                    forward_url = url_for(
                        "CategoryModelStudentView.show", pk=self.category_id
                    )
                else:
                    forward_url = url_for(
                        "TopicModelStudentView.show", pk=self.topic_id
                    )

        return forward_text, forward_url

    def get_assignment_progress(self, question_id):
        assignment_progress = None
        if self.is_random:
            return

        if self.assignment_id or self.category_id or self.topic_id:
            if self.assignment_id:
                questions = (
                    db.session.query(Question)
                    .join(assoc_assignment_question)
                    .join(Assignment)
                    .filter(Assignment.id == self.assignment_id)
                    .order_by(asc(Question.external_id))
                )
            elif self.category_id:
                questions = (
                    db.session.query(Question)
                    .filter_by(category_id=self.category_id)
                    .order_by(asc(Question.external_id))
                )
            else:
                questions = (
                    db.session.query(Question)
                    .filter_by(topic_id=self.topic_id)
                    .order_by(asc(Question.external_id))
                )
            i = 0
            for i, assigned_question in enumerate(questions, 1):
                if assigned_question.id == question_id:
                    break

            question_count = questions.count()
            percentage = 0 if question_count == 0 else round(i / question_count * 100)
            assignment_progress = {
                "done": i,
                "total": question_count,
                "percentage": percentage,
            }
        return assignment_progress

    def post_process_answer(
        self,
        form,
        is_answer_correct,
        question,
        message=None,
        options=None,
        back_count=1,
        render=True,
    ):
        self.update_redirect()

        # Check if user retries too fast
        min_retry_time = datetime.datetime.now() - datetime.timedelta(
            minutes=current_app.config["QUESTION_RETRY_MIN_MINUTES"]
        )
        min_retry_time_has_passed = (
            g.user.answered_questions.filter_by(question_id=question.id)
            .filter(AssocUserQuestion.created_on > min_retry_time)
            .first()
            is None
        )
        achievement = None

        if min_retry_time_has_passed:
            # Add entry to answered questions
            answered_question = AssocUserQuestion(
                is_answer_correct=is_answer_correct,
                question=question,
            )
            g.user.answered_questions.append(answered_question)
            commit_safely(db.session)

            achievement = check_for_new_achievement()
            if achievement:
                g.user.achievements.append(achievement)
                commit_safely(db.session)
        else:
            message = (
                "Da warst du wohl etwas zu schnell!<br>"
                f"Bitte warte {current_app.config['QUESTION_RETRY_MIN_MINUTES']} Minuten "
                "bevor du die selbe Frage nochmals beantwortest.<br>"
                "Die Beantwortung dieser Frage wurde nicht gewertet."
            )

        if message:
            category = (
                "success"
                if (is_answer_correct and min_retry_time_has_passed)
                else "danger"
            )
            flash(Markup(message), category)

        forward_text, forward_url = self.get_forward_button(question.id)
        assignment_progress = self.get_assignment_progress(question.id)
        self.extra_args = {
            "question": {
                "description": question.description_image_img(),
                "external_id": question.external_id,
                "category": question.category.name,
                "video_embed_url": question.video_embed_url(),
                "video_link_url": question.video_link_url(),
                "back_count": back_count,
                "forward_text": forward_text,
                "forward_url": forward_url,
                "assignment_progress": assignment_progress,
                "options": options,
            },
            "fire_confetti": is_answer_correct and min_retry_time_has_passed,
            "achievement": achievement,
        }

        if render:
            widgets = self._get_edit_widget(form=form)
            return self.render_template(
                self.form_template,
                title=self.form_title,
                widgets=widgets,
                appbuilder=self.appbuilder,
            )

    def pre_process_question(self, form):
        self.update_redirect()
        question = db.session.query(Question).filter_by(id=self.id).first()

        if question is None:
            description = "Diese Frage existiert nicht."
            external_id = None
            error = True
            assignment_progress = None
            category = None
        else:
            form.id.data = question.id
            description = question.description_image_img()
            external_id = question.external_id
            error = False
            assignment_progress = self.get_assignment_progress(question.id)
            category = question.category.name

        return question, description, external_id, error, assignment_progress, category

    def form_get(self, form):
        (
            question,
            description,
            external_id,
            error,
            assignment_progress,
            category,
        ) = self.pre_process_question(form)

        options = (
            self.form_get_additional_processing(form, question) if not error else None
        )

        self.extra_args = {
            "question": {
                "error": error,
                "description": description,
                "options": options,
                "external_id": external_id,
                "category": category,
                "submit_text": "Auswerten",
                "assignment_progress": assignment_progress,
            }
        }

    def form_get_additional_processing(self, form, question):
        # Implement in subclass
        pass


class QuestionSelfAssessedFormView(QuestionFormView):
    form = QuestionSelfAssessedForm
    form_title = "Selbstkontrolle"

    def form_get(self, form):
        is_answer_correct = False
        submit_text = None
        back_count = 1
        forward_text = None
        forward_url = None
        answer_value = None

        (
            question,
            description,
            external_id,
            error,
            assignment_progress,
            category,
        ) = self.pre_process_question(form)

        if not error:
            answer_value = request.args.get("answer")

            if answer_value:
                is_answer_correct = True if (answer_value == "CORRECT") else False

                self.post_process_answer(
                    form, is_answer_correct, question, back_count=2, render=False
                )
            else:
                forward_text, forward_url = None, None
                submit_text = "Auswerten"
                back_count = 1
                self.update_redirect()

        if not answer_value:
            self.extra_args = {
                "question": {
                    "description": description,
                    "external_id": external_id,
                    "category": category,
                    "submit_text": submit_text,
                    "back_count": back_count,
                    "forward_text": forward_text,
                    "forward_url": forward_url,
                    "assignment_progress": assignment_progress,
                },
                "fire_confetti": is_answer_correct,
            }

    def form_post(self, form):
        question_id = int(form.id.data)
        question = (
            db.session.query(Question)
            .filter_by(id=question_id, type=QuestionType.self_assessed.value)
            .first()
        )

        url = url_for(
            "QuestionSelfAssessedFormView.this_form_get",
            q_id=question.id,
            is_random=self.is_random,
            assignment_id=self.assignment_id,
            category_id=self.category_id,
            topic_id=self.topic_id,
        )

        solution_img = question.solution_image_img()
        correct_link = (
            f'<a class="btn btn-primary" href="{url}?answer=CORRECT">Richtig</a>'
        )
        incorrect_link = (
            f'<a class="btn btn-primary" href="{url}?answer=INCORRECT">Falsch</a>'
        )
        description = Markup(f"{solution_img}")
        after_description = Markup(f"{correct_link} {incorrect_link}")

        assignment_progress = self.get_assignment_progress(question_id)

        self.extra_args = {
            "question": {
                "description": description,
                "after_description": after_description,
                "external_id": question.external_id,
                "category": question.category.name,
                "submit_text": None,
                "video_embed_url": question.video_embed_url(),
                "video_link_url": question.video_link_url(),
                "assignment_progress": assignment_progress,
            }
        }

        widgets = self._get_edit_widget(form=form)
        return self.render_template(
            self.form_template,
            title=self.form_title,
            widgets=widgets,
            appbuilder=self.appbuilder,
        )


class Question2of5FormView(QuestionFormView):
    form = Question2of5Form
    form_title = "2 aus 5"

    def form_get_additional_processing(self, form, question):
        self.set_option_labels(form, question)

    @staticmethod
    def set_option_labels(form, question):
        form.checkbox1.label.text = question.get_option_image(question.option1_image)
        form.checkbox2.label.text = question.get_option_image(question.option2_image)
        form.checkbox3.label.text = question.get_option_image(question.option3_image)
        form.checkbox4.label.text = question.get_option_image(question.option4_image)
        form.checkbox5.label.text = question.get_option_image(question.option5_image)

    def form_post(self, form):
        question_id = int(form.id.data)
        result = (
            db.session.query(Question)
            .filter_by(id=question_id, type=QuestionType.two_of_five.value)
            .first()
        )
        self.set_option_labels(form, result)

        if result.option1_is_correct:
            form.checkbox1.render_kw = {"row_class": "success"}
        if result.option2_is_correct:
            form.checkbox2.render_kw = {"row_class": "success"}
        if result.option3_is_correct:
            form.checkbox3.render_kw = {"row_class": "success"}
        if result.option4_is_correct:
            form.checkbox4.render_kw = {"row_class": "success"}
        if result.option5_is_correct:
            form.checkbox5.render_kw = {"row_class": "success"}

        if form.checkbox1.data == result.option1_is_correct:
            form.checkbox1.description = "Richtig"
        else:
            form.checkbox1.description = "Falsch"
        if form.checkbox2.data == result.option2_is_correct:
            form.checkbox2.description = "Richtig"
        else:
            form.checkbox2.description = "Falsch"
        if form.checkbox3.data == result.option3_is_correct:
            form.checkbox3.description = "Richtig"
        else:
            form.checkbox3.description = "Falsch"
        if form.checkbox4.data == result.option4_is_correct:
            form.checkbox4.description = "Richtig"
        else:
            form.checkbox4.description = "Falsch"
        if form.checkbox5.data == result.option5_is_correct:
            form.checkbox5.description = "Richtig"
        else:
            form.checkbox5.description = "Falsch"

        if (
            (form.checkbox1.data == result.option1_is_correct)
            and (form.checkbox2.data == result.option2_is_correct)
            and (form.checkbox3.data == result.option3_is_correct)
            and (form.checkbox4.data == result.option4_is_correct)
            and (form.checkbox5.data == result.option5_is_correct)
        ):
            message = "<strong>RICHTIG!</strong>"
            is_answer_correct = True
        else:
            message = "<strong>FALSCH!</strong>"
            is_answer_correct = False

        return self.post_process_answer(form, is_answer_correct, result, message)


class Question1of6FormView(QuestionFormView):
    form = Question1of6Form
    form_title = "1 aus 6"

    def form_get_additional_processing(self, form, question):
        self.set_option_labels(form, question)

    @staticmethod
    def set_option_labels(form, question):
        form.checkbox1.label.text = question.get_option_image(question.option1_image)
        form.checkbox2.label.text = question.get_option_image(question.option2_image)
        form.checkbox3.label.text = question.get_option_image(question.option3_image)
        form.checkbox4.label.text = question.get_option_image(question.option4_image)
        form.checkbox5.label.text = question.get_option_image(question.option5_image)
        form.checkbox6.label.text = question.get_option_image(question.option6_image)

    def form_post(self, form):
        question_id = int(form.id.data)
        question = (
            db.session.query(Question)
            .filter_by(id=question_id, type=QuestionType.one_of_six.value)
            .first()
        )
        self.set_option_labels(form, question)

        if question.option1_is_correct:
            form.checkbox1.render_kw = {"row_class": "success"}
        if question.option2_is_correct:
            form.checkbox2.render_kw = {"row_class": "success"}
        if question.option3_is_correct:
            form.checkbox3.render_kw = {"row_class": "success"}
        if question.option4_is_correct:
            form.checkbox4.render_kw = {"row_class": "success"}
        if question.option5_is_correct:
            form.checkbox5.render_kw = {"row_class": "success"}
        if question.option6_is_correct:
            form.checkbox6.render_kw = {"row_class": "success"}

        if form.checkbox1.data == question.option1_is_correct:
            form.checkbox1.description = "Richtig"
        else:
            form.checkbox1.description = "Falsch"
        if form.checkbox2.data == question.option2_is_correct:
            form.checkbox2.description = "Richtig"
        else:
            form.checkbox2.description = "Falsch"
        if form.checkbox3.data == question.option3_is_correct:
            form.checkbox3.description = "Richtig"
        else:
            form.checkbox3.description = "Falsch"
        if form.checkbox4.data == question.option4_is_correct:
            form.checkbox4.description = "Richtig"
        else:
            form.checkbox4.description = "Falsch"
        if form.checkbox5.data == question.option5_is_correct:
            form.checkbox5.description = "Richtig"
        else:
            form.checkbox5.description = "Falsch"
        if form.checkbox6.data == question.option6_is_correct:
            form.checkbox6.description = "Richtig"
        else:
            form.checkbox6.description = "Falsch"

        if (
            (form.checkbox1.data == question.option1_is_correct)
            and (form.checkbox2.data == question.option2_is_correct)
            and (form.checkbox3.data == question.option3_is_correct)
            and (form.checkbox4.data == question.option4_is_correct)
            and (form.checkbox5.data == question.option5_is_correct)
            and (form.checkbox6.data == question.option6_is_correct)
        ):
            message = "<strong>RICHTIG!</strong>"
            is_answer_correct = True
        else:
            message = "<strong>FALSCH!</strong>"
            is_answer_correct = False

        return self.post_process_answer(form, is_answer_correct, question, message)


class Question3to3FormView(QuestionFormView):
    form = Question3to3Form
    form_title = "Lückentext"

    form_fieldsets = [
        ("1", {"fields": ["checkbox1a", "checkbox1b", "checkbox1c"]}),
        ("2", {"fields": ["checkbox2a", "checkbox2b", "checkbox2c"]}),
    ]

    def form_get_additional_processing(self, form, question):
        self.set_option_labels(form, question)

    @staticmethod
    def set_option_labels(form, question):
        form.checkbox1a.label.text = question.get_option_small_image(
            question.option1a_image
        )
        form.checkbox1b.label.text = question.get_option_small_image(
            question.option1b_image
        )
        form.checkbox1c.label.text = question.get_option_small_image(
            question.option1c_image
        )
        form.checkbox2a.label.text = question.get_option_small_image(
            question.option2a_image
        )
        form.checkbox2b.label.text = question.get_option_small_image(
            question.option2b_image
        )
        form.checkbox2c.label.text = question.get_option_small_image(
            question.option2c_image
        )

    def form_post(self, form):
        question_id = int(form.id.data)
        question = (
            db.session.query(Question)
            .filter_by(id=question_id, type=QuestionType.three_to_three.value)
            .first()
        )
        self.set_option_labels(form, question)

        if question.option1a_is_correct:
            form.checkbox1a.render_kw = {"row_class": "success"}
        if question.option1b_is_correct:
            form.checkbox1b.render_kw = {"row_class": "success"}
        if question.option1c_is_correct:
            form.checkbox1c.render_kw = {"row_class": "success"}
        if question.option2a_is_correct:
            form.checkbox2a.render_kw = {"row_class": "success"}
        if question.option2b_is_correct:
            form.checkbox2b.render_kw = {"row_class": "success"}
        if question.option2c_is_correct:
            form.checkbox2c.render_kw = {"row_class": "success"}

        if form.checkbox1a.data == question.option1a_is_correct:
            form.checkbox1a.description = "Richtig"
        else:
            form.checkbox1a.description = "Falsch"
        if form.checkbox1b.data == question.option1b_is_correct:
            form.checkbox1b.description = "Richtig"
        else:
            form.checkbox1b.description = "Falsch"
        if form.checkbox1c.data == question.option1c_is_correct:
            form.checkbox1c.description = "Richtig"
        else:
            form.checkbox1c.description = "Falsch"
        if form.checkbox2a.data == question.option2a_is_correct:
            form.checkbox2a.description = "Richtig"
        else:
            form.checkbox2a.description = "Falsch"
        if form.checkbox2b.data == question.option2b_is_correct:
            form.checkbox2b.description = "Richtig"
        else:
            form.checkbox2b.description = "Falsch"
        if form.checkbox2c.data == question.option2c_is_correct:
            form.checkbox2c.description = "Richtig"
        else:
            form.checkbox2c.description = "Falsch"

        if (
            (form.checkbox1a.data == question.option1a_is_correct)
            and (form.checkbox1b.data == question.option1b_is_correct)
            and (form.checkbox1c.data == question.option1c_is_correct)
            and (form.checkbox2a.data == question.option2a_is_correct)
            and (form.checkbox2b.data == question.option2b_is_correct)
            and (form.checkbox2c.data == question.option2c_is_correct)
        ):
            message = "<strong>RICHTIG!</strong>"
            is_answer_correct = True
        else:
            message = "<strong>FALSCH!</strong>"
            is_answer_correct = False

        return self.post_process_answer(form, is_answer_correct, question, message)


class Question2DecimalsFormView(QuestionFormView):
    form = Question2DecimalsForm
    form_title = "Werteingabe zwei Zahlen"

    def form_get_additional_processing(self, form, question):
        return {"show_help_button": True}

    def form_post(self, form):
        question_id = int(form.id.data)
        question = (
            db.session.query(Question)
            .filter_by(id=question_id, type=QuestionType.two_decimals.value)
            .first()
        )

        value1_correct = False
        value2_correct = False
        if (form.value1.data <= question.value1_upper_limit) and (
            form.value1.data >= question.value1_lower_limit
        ):
            form.value1.description = "Richtig"
            value1_correct = True
        else:
            form.value1.description = "Falsch"

        if (form.value2.data <= question.value2_upper_limit) and (
            form.value2.data >= question.value2_lower_limit
        ):
            form.value2.description = "Richtig"
            value2_correct = True
        else:
            form.value2.description = "Falsch"

        if value1_correct and value2_correct:
            message = "<strong>RICHTIG!</strong>"
            is_answer_correct = True
        else:
            message = (
                "<strong><div>FALSCH! Richtig gewesen"
                f" wäre:</div><div>{question.value1_lower_limit} ≤ Ergebnis 1 ≤"
                f" {question.value1_upper_limit}</div><div>{question.value2_lower_limit} ≤"
                f" Ergebnis 2 ≤ {question.value2_upper_limit}</div></strong>"
            )
            is_answer_correct = False

        return self.post_process_answer(form, is_answer_correct, question, message)


class Question1DecimalFormView(QuestionFormView):
    form = Question1DecimalForm
    form_title = "Werteingabe eine Zahl"

    def form_get_additional_processing(self, form, question):
        return {"show_help_button": True}

    def form_post(self, form):
        question_id = int(form.id.data)
        question = (
            db.session.query(Question)
            .filter_by(id=question_id, type=QuestionType.one_decimal.value)
            .first()
        )

        if (form.value.data <= question.value1_upper_limit) and (
            form.value.data >= question.value1_lower_limit
        ):
            form.value.description = "Richtig"
            message = "<strong>RICHTIG!</strong>"
            is_answer_correct = True
        else:
            message = (
                "<strong><div>FALSCH! Richtig gewesen"
                f" wäre:</div><div>{question.value1_lower_limit} ≤ Ergebnis ≤"
                f" {question.value1_upper_limit}</div></strong>"
            )
            is_answer_correct = False

        return self.post_process_answer(form, is_answer_correct, question, message)


class QuestionSelect4FormView(QuestionFormView):
    form = QuestionSelect4Form
    form_title = "Zuordnung"

    form_fieldsets = [
        (
            "Antworten",
            {"fields": ["selection1", "selection2", "selection3", "selection4"]},
        ),
    ]

    def form_get_additional_processing(self, form, question):
        return self.set_and_get_option_labels(form, question)

    def form_post(self, form):
        question_id = int(form.id.data)
        question = (
            db.session.query(Question)
            .filter_by(id=question_id, type=QuestionType.select_four.value)
            .first()
        )
        options = self.set_and_get_option_labels(form, question)

        if form.selection1.data == question.selection1_solution.value:
            form.selection1.description = "Richtig"
        else:
            form.selection1.description = "Falsch"
        if form.selection2.data == question.selection2_solution.value:
            form.selection2.description = "Richtig"
        else:
            form.selection2.description = "Falsch"
        if form.selection3.data == question.selection3_solution.value:
            form.selection3.description = "Richtig"
        else:
            form.selection3.description = "Falsch"
        if form.selection4.data == question.selection4_solution.value:
            form.selection4.description = "Richtig"
        else:
            form.selection4.description = "Falsch"

        if (
            (form.selection1.data == question.selection1_solution.value)
            and (form.selection2.data == question.selection2_solution.value)
            and (form.selection3.data == question.selection3_solution.value)
            and (form.selection4.data == question.selection4_solution.value)
        ):
            message = "<strong>RICHTIG!</strong>"
            is_answer_correct = True
        else:
            message = "<strong>FALSCH!</strong>"
            is_answer_correct = False

        return self.post_process_answer(
            form, is_answer_correct, question, message, options
        )

    @staticmethod
    def set_and_get_option_labels(form, result):
        form.selection1.label.text = result.get_selection_image(result.selection1_image)
        form.selection2.label.text = result.get_selection_image(result.selection2_image)
        form.selection3.label.text = result.get_selection_image(result.selection3_image)
        form.selection4.label.text = result.get_selection_image(result.selection4_image)
        options = {
            "A": result.get_option_small_image(result.option1_image),
            "B": result.get_option_small_image(result.option2_image),
            "C": result.get_option_small_image(result.option3_image),
            "D": result.get_option_small_image(result.option4_image),
            "E": result.get_option_small_image(result.option5_image),
            "F": result.get_option_small_image(result.option6_image),
        }
        return options


class DeleteStatsFormView(SimpleFormView):
    form = DeleteStatsForm
    form_title = "Benutzerstatistik löschen"
    form_template = "edit_additional.html"
    edit_widget = ExtendedEditWidget
    extra_args = {
        "question": {
            "description": (
                "Die Benutzerstatistik beinhaltet alle bereits gelösten Aufgaben und freigeschalteten Errungenschaften."
            ),
            "submit_text": "Löschen",
        }
    }

    def form_post(self, form):
        db.session.query(AssocUserQuestion).filter_by(user_id=g.user.id).delete()
        g.user.achievements.clear()
        commit_safely(db.session)
        flash("Benutzerstatistik gelöscht", "info")


class DeleteAccountFormView(SimpleFormView):
    form = DeleteAccountForm
    form_title = "Benutzerkonto löschen"
    email_subject = current_app.config["APP_NAME"] + " - Benutzerkonto löschen"
    form_template = "edit_additional.html"
    edit_widget = ExtendedEditWidget
    extra_args = {
        "question": {
            "description": (
                "Nach dem Löschen des Benutzerkontos ist keine weitere Nutzung der Seite mehr möglich, "
                "ohne sich erneut zu registrieren."
            ),
            "submit_text": "Löschen",
        }
    }
    email_template = "account_delete_mail.html"

    def send_email(self, user):
        url = url_for(
            "ExtendedUserDBModelView.confirm_account_delete",
            _external=True,
            user_id=user.id,
            token=user.account_delete_token,
        )
        html = self.render_template(
            self.email_template,
            url=url,
            username=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
        )
        return send_email(self.appbuilder.get_app, self.email_subject, html, user.email)

    def form_post(self, form):
        if g.user.email_confirmation_token:
            flash("Bitte bestätige zuerst deine E-Mail-Adresse.", category="danger")
            return

        appbuilder.sm.set_account_delete_token(g.user)
        mail_is_sent = self.send_email(g.user)
        if mail_is_sent:
            flash(
                "Um die Löschung zu bestätigen, wurde eine E-Mail an dich gesendet.",
                category="info",
            )
        else:
            flash(
                "Versenden der E-Mail zur Bestätigung der Löschung des Benutzerkontos fehlgeschlagen. "
                "Bitte versuche es später erneut",
                category="danger",
            )


class ImportUsersFormView(SimpleFormView):
    form = ImportUsersForm
    form_title = "Schüler importieren"
    form_template = "edit_additional.html"
    extra_args = dict(
        question=dict(
            description_include="import_user_description.html",
            max_imports_per_day=current_app.config["MAX_USER_IMPORTS_PER_DAY"],
        )
    )

    def form_post(self, form):
        appbuilder.sm.import_users(form.file.data)
        return redirect(url_for(f"{self.__class__.__name__}.this_form_get"))


class AddQuestionToAssignmentFormView(SimpleFormView):
    form = AddQuestionToAssignmentForm
    edit_widget = FormMinimalInlineWidget

    question_model = SQLAInterface(Question, db.session)
    assignment_model = SQLAInterface(Assignment, db.session)

    @expose("/form", methods=["POST"])
    @has_access
    def this_form_post(self):
        self._init_vars()
        form = self.form.refresh()

        if form.validate_on_submit():
            response = self.form_post(form)
            if not response:
                return redirect(self.get_redirect())
            return response
        else:
            abort(404)

    def form_post(self, form):
        assignment = self.assignment_model.get(form.assignment_id.raw_data[0])
        if not assignment or assignment.created_by == g.user:
            abort(404)

        if form.question_id.data:
            question_ids = [form.question_id.data]
        else:
            question_ids = session.pop("question_ids_to_add_to_assignment", None)

        if not question_ids:
            abort(404)

        for question_id in question_ids:
            question = self.question_model.get(question_id)
            if not question:
                abort(404)

            assignment.assigned_questions.append(question)
        if self.assignment_model.edit(assignment):
            return make_response(jsonify(""))
