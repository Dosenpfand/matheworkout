from random import randrange

from flask import url_for, Response, flash
from flask_appbuilder import BaseView, has_access, expose
from werkzeug.utils import redirect

from app import db, appbuilder
from app.models.general import QuestionType, Question, Assignment
from app.utils.general import get_question_count


class QuestionRandom(BaseView):
    route_base = "/"

    @has_access
    @expose("questionrandom/")
    def question_random(self):
        type_id_to_form = {
            0: QuestionType.two_of_five.value,
            1: QuestionType.one_of_six.value,
            2: QuestionType.three_to_three.value,
            3: QuestionType.two_decimals.value,
            4: QuestionType.one_decimal.value,
            5: QuestionType.self_assessed.value,
            6: QuestionType.select_four.value,
        }

        type_id_to_count = {}
        for q_id, class_name in type_id_to_form.items():
            type_id_to_count[q_id] = get_question_count(class_name)

        total_count = sum(type_id_to_count.values())

        if total_count == 0:
            flash('Keine Aufgaben vorhanden', 'error')
            return redirect(appbuilder.get_url_for_index)
        else:
            rand_id = randrange(0, total_count)

            if rand_id < type_id_to_count[0]:
                rand_form = 'Question2of5FormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1]):
                rand_form = 'Question1of6FormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1] + type_id_to_count[2]):
                rand_form = 'Question3to3FormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1] + type_id_to_count[2] + type_id_to_count[3]):
                rand_form = 'Question2DecimalsFormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1] + type_id_to_count[2] + type_id_to_count[3] +
                            type_id_to_count[4]):
                rand_form = 'Question1DecimalFormView'
            elif rand_id < (type_id_to_count[0] + type_id_to_count[1] + type_id_to_count[2] + type_id_to_count[3] +
                            type_id_to_count[4] + type_id_to_count[5]):
                rand_form = 'QuestionSelfAssessedFormView'
            else:
                rand_form = 'QuestionSelect4FormView'

        return redirect(url_for(f'{rand_form}.this_form_get'))


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
