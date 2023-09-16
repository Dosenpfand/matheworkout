from flask import url_for, Response, flash, g, abort
from flask_appbuilder import BaseView, has_access, expose, action
from flask_appbuilder.models.sqla.interface import SQLAInterface
from sqlalchemy import func
from sqlalchemy.orm import load_only
from werkzeug.utils import redirect

from app import db
from app.forms.forms import AddQuestionToAssignmentForm
from app.models.general import Achievement
from app.models.general import QuestionType, Question, Assignment, Topic, LearningGroup
from app.views.widgets import ExtendedShowWidget, FormMinimalInlineWidget


class QuestionRandom(BaseView):
    route_base = "/"

    @staticmethod
    def get_random_question(topic=None):
        if not topic:
            return (
                db.session.query(Question)
                .join(Topic)
                .filter(Topic.school_type == g.user.school_type)
                .options(load_only("id"))
                .order_by(func.random())
                .first()
            )
        else:
            return (
                db.session.query(Question)
                .options(load_only("id", "topic_id"))
                .filter_by(topic_id=topic.id)
                .offset(
                    func.floor(
                        func.random()
                        * db.session.query(func.count(Question.id)).filter_by(
                            topic_id=topic.id
                        )
                    )
                )
                .first()
            )

    @has_access
    @expose("/questionrandom/")
    @expose("/questionrandom/topic/<int:topic_id>")
    def random_question_redirect(self, topic_id=None):
        if topic_id:
            topic = db.session.query(Topic).filter_by(id=topic_id).first()
        else:
            topic = None

        question = self.get_random_question(topic)
        if not question:
            flash("Keine Aufgabe gefunden.", category="danger")
            return redirect(self.appbuilder.get_url_for_index)

        type_to_form = {
            QuestionType.two_of_five: "Question2of5FormView",
            QuestionType.one_of_six: "Question1of6FormView",
            QuestionType.three_to_three: "Question3to3FormView",
            QuestionType.two_decimals: "Question2DecimalsFormView",
            QuestionType.one_decimal: "Question1DecimalFormView",
            QuestionType.self_assessed: "QuestionSelfAssessedFormView",
            QuestionType.select_four: "QuestionSelect4FormView",
            QuestionType.select_two: "QuestionSelect2FormView",
        }
        form = type_to_form[question.type]
        return redirect(
            url_for(
                f"{form}.this_form_get",
                q_id=question.id,
                topic_id=topic_id,
                is_random=True,
            )
        )


class IdToForm(BaseView):
    route_base = "/"

    @has_access
    @expose("idtoform/<int:q_id>")
    @expose("idtoform/<int:q_id>/assignment/<int:assignment_id>")
    @expose("idtoform/<int:q_id>/category/<int:category_id>")
    @expose("idtoform/<int:q_id>/topic/<int:topic_id>")
    def id_to_form(self, q_id, assignment_id=None, category_id=None, topic_id=None):
        question = db.session.query(Question).filter_by(id=q_id).first()
        if not question:
            abort(404)
        question_type = question.type.value

        type_to_form = {
            QuestionType.two_of_five.value: "Question2of5FormView",
            QuestionType.one_of_six.value: "Question1of6FormView",
            QuestionType.three_to_three.value: "Question3to3FormView",
            QuestionType.two_decimals.value: "Question2DecimalsFormView",
            QuestionType.one_decimal.value: "Question1DecimalFormView",
            QuestionType.self_assessed.value: "QuestionSelfAssessedFormView",
            QuestionType.select_four.value: "QuestionSelect4FormView",
            QuestionType.select_two.value: "QuestionSelect2FormView",
        }

        form = type_to_form[question_type]
        url = url_for(
            f"{form}.this_form_get",
            q_id=q_id,
            assignment_id=assignment_id,
            category_id=category_id,
            topic_id=topic_id,
        )

        return redirect(url)


class AssignmentModelEvaluationView(BaseView):
    default_view = "show"

    @expose("/show/<int:assignment_id>")
    @has_access
    def show(self, assignment_id):
        self.update_redirect()
        questions, state_users_questions, users = self.get_assignment_data(
            assignment_id
        )

        if not questions:
            abort(404)

        return self.render_template(
            "assignment_teacher_view.html",
            users=users,
            questions=questions,
            state_users_questions=state_users_questions,
            title="Auswertung",
        )

    @expose("/export/<int:assignment_id>")
    @has_access
    def export(self, assignment_id):
        self.update_redirect()
        questions, state_users_questions, users = self.get_assignment_data(
            assignment_id
        )

        if not questions:
            abort(404)

        content = self.render_template(
            "assignment_teacher_export.html",
            users=users,
            questions=questions,
            state_users_questions=state_users_questions,
            title="Export",
        )

        return Response(content, content_type="text/csv")

    @staticmethod
    def get_assignment_data(assignment_id):
        assignment = (
            db.session.query(Assignment)
            .filter_by(id=assignment_id, created_by_fk=g.user.id)
            .first()
        )

        if not assignment or not assignment.learning_group:
            return [], [], []

        users = assignment.learning_group.users
        questions = assignment.assigned_questions
        state_users_questions = {}
        for user in users:
            state_users_questions[user.id] = {}
            for question in questions:
                state_users_questions[user.id][question.id] = question.state_user(
                    user.id
                )
        return questions, state_users_questions, users


class UtilExtendedView(BaseView):
    route_base = ""
    default_view = "back"

    @expose("/back_mult/<int:count>")
    def back_mult(self, count):
        for i in range(count - 1):
            self.get_redirect()
        return redirect(self.get_redirect())


class JoinLearningGroup(BaseView):
    route_base = ""

    @expose("/join_learning_group/<int:group_id>/<string:join_token>")
    @has_access
    def join_learning_group(self, group_id, join_token):
        learning_group = db.session.query(LearningGroup).filter_by(id=group_id).first()
        if learning_group:
            if g.user in learning_group.users:
                flash("Du bist bereits Mitglied dieser Klasse", "danger")
            elif join_token == learning_group.join_token:
                learning_group.users.append(g.user)
                db.session.commit()
                flash("Du bist erfolgreich der Klasse beigetreten", "success")
            else:
                flash("Klasse beitreten fehlgeschlagen", "danger")
        else:
            flash("Klasse nicht gefunden", "danger")

        return redirect(url_for("ExtendedIndexView.index"))


class DataProtectionView(BaseView):
    route_base = ""
    default_view = "data_protection"
    template = "data_protection.html"

    @expose("/data_protection")
    def data_protection(self):
        self.update_redirect()
        return self.render_template(
            self.template, appbuilder=self.appbuilder, title="Datenschutz"
        )


class ImprintView(BaseView):
    route_base = ""
    default_view = "imprint"
    template = "imprint.html"

    @expose("/imprint")
    def imprint(self):
        self.update_redirect()
        return self.render_template(
            self.template, appbuilder=self.appbuilder, title="Impressum"
        )


class SupportView(BaseView):
    route_base = ""
    default_view = "support"
    template = "support.html"

    @expose("/support")
    def support(self):
        self.update_redirect()
        return self.render_template(
            self.template, appbuilder=self.appbuilder, title="Unterstützung"
        )


class AchievementsView(BaseView):
    route_base = ""
    default_view = "achievements"
    template = "achievements.html"

    @expose("/achievements")
    def achievements(self):
        self.update_redirect()

        achievements = db.session.query(Achievement).all()

        return self.render_template(
            self.template,
            appbuilder=self.appbuilder,
            title="Errungenschaften",
            achievements=achievements,
        )


class ShowQuestionDetailsMixIn:
    questions_col_name = "questions"
    show_details_widget = ExtendedShowWidget
    add_question_to_assignment_widget = FormMinimalInlineWidget
    add_question_to_assignment_form = AddQuestionToAssignmentForm
    question_model = SQLAInterface(Question, db.session)

    def __init__(self):
        if not self.extra_args:
            self.extra_args = None

    def _get_show_details_widget(self, widgets=None):
        widgets = widgets or {}
        widgets["show_details"] = self.show_details_widget(route_base=self.route_base)
        widgets["add_question_to_assignment"] = self.add_question_to_assignment_widget(
            route_base=self.route_base
        )
        return widgets

    @has_access
    @expose("/show_question_details/<pk>", methods=["GET"])
    def show_question_details(self, pk):
        pk = self._deserialize_pk_if_composite(pk)

        item = self.datamodel.get(pk, self._base_filters)
        if not item:
            abort(404)

        questions = []
        widgets = self._get_show_details_widget()

        for question in getattr(item, self.questions_col_name):
            add_to_assignment_form = self.add_question_to_assignment_form.refresh()
            add_to_assignment_form.question_id.data = question.id

            current_question = {
                "error": False,
                "description": question.description_image_img(),
                "external_id": question.external_id,
                "category": question.category.name,
                "add_to_assignment_form": add_to_assignment_form,
                "solution": question.get_solution(),
            }
            # TODO: should be handled in Question class
            if question.type == QuestionType.one_of_six:
                current_question["cells"] = [
                    question.get_option_image(question.option1_image),
                    question.get_option_image(question.option2_image),
                    question.get_option_image(question.option3_image),
                    question.get_option_image(question.option4_image),
                    question.get_option_image(question.option5_image),
                    question.get_option_image(question.option6_image),
                ]
            elif question.type == QuestionType.two_of_five:
                current_question["cells"] = [
                    question.get_option_image(question.option1_image),
                    question.get_option_image(question.option2_image),
                    question.get_option_image(question.option3_image),
                    question.get_option_image(question.option4_image),
                    question.get_option_image(question.option5_image),
                ]
            elif question.type == QuestionType.three_to_three:
                current_question["cellsets"] = [
                    ("1", {"fields": ["checkbox1a", "checkbox1b", "checkbox1c"]}),
                    ("2", {"fields": ["checkbox2a", "checkbox2b", "checkbox2c"]}),
                ]

                current_question["cells"] = {
                    "checkbox1a": (
                        "",
                        question.get_option_small_image(question.option1a_image),
                    ),
                    "checkbox1b": (
                        "",
                        question.get_option_small_image(question.option1b_image),
                    ),
                    "checkbox1c": (
                        "",
                        question.get_option_small_image(question.option1c_image),
                    ),
                    "checkbox2a": (
                        "",
                        question.get_option_small_image(question.option2a_image),
                    ),
                    "checkbox2b": (
                        "",
                        question.get_option_small_image(question.option2b_image),
                    ),
                    "checkbox2c": (
                        "",
                        question.get_option_small_image(question.option2c_image),
                    ),
                }
            elif question.type == QuestionType.select_four:
                current_question["cellsets"] = [
                    (
                        "Antworten",
                        {
                            "fields": [
                                "selection1",
                                "selection2",
                                "selection3",
                                "selection4",
                            ]
                        },
                    ),
                    (
                        "Optionen",
                        {
                            "fields": [
                                "option1",
                                "option2",
                                "option3",
                                "option4",
                                "option5",
                                "option6",
                            ]
                        },
                    ),
                ]

                current_question["cells"] = {
                    "option1": (
                        "A",
                        question.get_option_small_image(question.option1_image),
                    ),
                    "option2": (
                        "B",
                        question.get_option_small_image(question.option2_image),
                    ),
                    "option3": (
                        "C",
                        question.get_option_small_image(question.option3_image),
                    ),
                    "option4": (
                        "D",
                        question.get_option_small_image(question.option4_image),
                    ),
                    "option5": (
                        "E",
                        question.get_option_small_image(question.option5_image),
                    ),
                    "option6": (
                        "F",
                        question.get_option_small_image(question.option6_image),
                    ),
                    "selection1": (
                        " ",
                        question.get_option_small_image(question.selection1_image),
                    ),
                    "selection2": (
                        " ",
                        question.get_option_small_image(question.selection2_image),
                    ),
                    "selection3": (
                        " ",
                        question.get_option_small_image(question.selection3_image),
                    ),
                    "selection4": (
                        " ",
                        question.get_option_small_image(question.selection4_image),
                    ),
                }
            elif question.type == QuestionType.select_two:
                current_question["cellsets"] = [
                    (
                        "Antworten",
                        {
                            "fields": [
                                "selection1",
                                "selection2",
                            ]
                        },
                    ),
                    (
                        "Optionen",
                        {
                            "fields": [
                                "option1",
                                "option2",
                                "option3",
                                "option4",
                            ]
                        },
                    ),
                ]

                current_question["cells"] = {
                    "option1": (
                        "A",
                        question.get_option_small_image(question.option1_image),
                    ),
                    "option2": (
                        "B",
                        question.get_option_small_image(question.option2_image),
                    ),
                    "option3": (
                        "C",
                        question.get_option_small_image(question.option3_image),
                    ),
                    "option4": (
                        "D",
                        question.get_option_small_image(question.option4_image),
                    ),
                    "selection1": (
                        " ",
                        question.get_option_small_image(question.selection1_image),
                    ),
                    "selection2": (
                        " ",
                        question.get_option_small_image(question.selection2_image),
                    ),
                }

            questions.append(current_question)

        self.extra_args = {"questions": questions}
        return self.render_template(
            "edit_additional_multiple.html",
            widgets=widgets,
            form_action=url_for("AddQuestionToAssignmentFormView.this_form_post"),
            title="Aufgaben",
        )

    @action(
        "show_question_details_action",
        "Alle Aufgaben anzeigen",
        confirmation=None,
        icon="fa-magnifying-glass",
        multiple=False,
    )
    def show_question_details_action(self, item):
        url = url_for(f"{self.__class__.__name__}.show_question_details", pk=item.id)
        return redirect(url)
