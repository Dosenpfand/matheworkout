from flask import g
from flask_appbuilder.models.filters import BaseFilter
from flask_appbuilder.models.sqla.filters import get_field_setup_query

from app.models.general import Question


class FilterInFunctionWithNone(BaseFilter):
    name = (
        "Filter view where field is in a list returned by a function supporting None"
        " being in the list"
    )
    arg_name = "infwnone"

    def apply(self, query, func):
        query, field = get_field_setup_query(query, self.model, self.column_name)
        func_ret_list = func()

        if None in func_ret_list:
            filter_arg = field.in_(func_ret_list) | (field == None)  # noqa
        else:
            filter_arg = field.in_(func_ret_list)
        return query.filter(filter_arg)


class FilterQuestionByAnsweredCorrectness(BaseFilter):
    name = "Filters for (in)correctly answered questions"
    arg_name = None

    def apply(self, query, is_answer_correct):
        return query.filter(
            Question.answered_users.any(
                user_id=g.user.id,
                is_answer_correct=is_answer_correct,
            )
        )


class FilterQuestionByNotAnsweredCorrectness(BaseFilter):
    name = "Filters for not (in)correctly answered questions"
    arg_name = None

    def apply(self, query, is_answer_correct):
        return query.filter(
            ~Question.answered_users.any(
                user_id=g.user.id, is_answer_correct=is_answer_correct
            )
        )
