from random import randrange

from flask import url_for, Response, flash
from flask_appbuilder import BaseView, has_access, expose
from sqlalchemy import func
from sqlalchemy.orm import load_only
from werkzeug.utils import redirect

from app import db
from app.models.general import QuestionType, Question, Assignment, Topic


class QuestionRandom(BaseView):
    route_base = "/"

    def get_random_question(self, topic=None):
        if not topic:
            return db.session.query(Question).options(load_only('id')).offset(
                func.floor(func.random() * db.session.query(func.count(Question.id)))
            ).first()
        else:
            return db.session.query(Question).options(load_only('id', 'topic_id')).filter_by(topic_id=topic.id).offset(
                func.floor(func.random() * db.session.query(func.count(Question.id)).filter_by(topic_id=topic.id))
            ).first()

    @has_access
    @expose("/questionrandom/")
    @expose("/questionrandom/topic/<int:topic_id>")
    def random_question_redirect(self, topic_id=None):
        if topic_id:
            topic = db.session.query(Topic).filter_by(id=topic_id).first()
        else:
            topic = None

        question = self.get_random_question(topic)
        type_to_form = {
            QuestionType.two_of_five: 'Question2of5FormView',
            QuestionType.one_of_six: 'Question1of6FormView',
            QuestionType.three_to_three: 'Question3to3FormView',
            QuestionType.two_decimals: 'Question2DecimalsFormView',
            QuestionType.one_decimal: 'Question1DecimalFormView',
            QuestionType.self_assessed: 'QuestionSelfAssessedFormView',
            QuestionType.select_four: 'QuestionSelect4FormView',
        }
        form = type_to_form[question.type]
        return redirect(url_for(f'{form}.this_form_get', q_id=question.id))


class IdToForm(BaseView):
    route_base = '/'

    @has_access
    @expose('idtoform/<int:q_id>')
    @expose('idtoform/<int:q_id>/assignment/<int:assignment_id>')
    @expose('idtoform/<int:q_id>/category/<int:category_id>')
    def id_to_form(self, q_id, assignment_id=None, category_id=None):
        question = db.session.query(Question).filter_by(id=q_id).first()
        question_type = question.type.value

        type_to_form = {
            QuestionType.two_of_five.value: 'Question2of5FormView',
            QuestionType.one_of_six.value: 'Question1of6FormView',
            QuestionType.three_to_three.value: 'Question3to3FormView',
            QuestionType.two_decimals.value: 'Question2DecimalsFormView',
            QuestionType.one_decimal.value: 'Question1DecimalFormView',
            QuestionType.self_assessed.value: 'QuestionSelfAssessedFormView',
            QuestionType.select_four.value: 'QuestionSelect4FormView',
        }

        form = type_to_form[question_type]
        url = url_for(f'{form}.this_form_get', q_id=q_id, assignment_id=assignment_id, category_id=category_id)

        return redirect(url)


class AssignmentModelTeacherView(BaseView):
    default_view = 'show'

    @expose('/show/<int:assignment_id>')
    @has_access
    def show(self, assignment_id):
        self.update_redirect()
        questions, state_users_questions, users = self.get_assignment_data(assignment_id)

        return self.render_template('assignment_teacher_view.html', users=users, questions=questions,
                                    state_users_questions=state_users_questions)

    @expose('/export/<int:assignment_id>')
    @has_access
    def export(self, assignment_id):
        self.update_redirect()
        questions, state_users_questions, users = self.get_assignment_data(assignment_id)
        content = self.render_template('assignment_teacher_export.html', users=users, questions=questions,
                                       state_users_questions=state_users_questions)

        return Response(content, content_type='text/csv')

    @staticmethod
    def get_assignment_data(assignment_id):
        assignment = db.session.query(Assignment).filter_by(id=assignment_id).first()

        if not assignment:
            return [], [], []

        users = assignment.learning_group.users
        questions = assignment.assigned_questions
        state_users_questions = {}
        for user in users:
            state_users_questions[user.id] = {}
            for question in questions:
                state_users_questions[user.id][question.id] = question.state_user(user.id)
        return questions, state_users_questions, users


class UtilExtendedView(BaseView):
    route_base = ''
    default_view = 'back'

    @expose("/back_mult/<int:count>")
    def back_mult(self, count):
        for i in range(count - 1):
            self.get_redirect()
        return redirect(self.get_redirect())
