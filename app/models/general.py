import datetime
import enum
import operator
import re
import secrets
from functools import reduce
from itertools import groupby
from urllib.parse import urlparse, parse_qs

from flask import Markup, g, url_for, request
from flask_appbuilder import Model
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.models.mixins import ImageColumn, AuditMixin
from flask_appbuilder.security.sqla.models import User, RegisterUser
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    Boolean,
    Float,
    Enum,
    DateTime,
    Sequence,
    Table,
)
from sqlalchemy.orm import relationship, validates


class Select4Enum(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"
    E = "E"
    F = "F"

    @staticmethod
    def get_values():
        return [el.value for el in Select4Enum]


assoc_user_learning_group = Table(
    "assoc_user_learning_group",
    Model.metadata,
    Column("user_id", ForeignKey("ab_user.id"), primary_key=True),
    Column("learning_group_id", ForeignKey("learning_group.id"), primary_key=True),
)
assoc_assignment_question = Table(
    "assoc_assignment_question",
    Model.metadata,
    Column("assignment_id", ForeignKey("assignment.id"), primary_key=True),
    Column("question_id", ForeignKey("question.id"), primary_key=True),
)


class Topic(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(500), nullable=False)
    questions = relationship(
        "Question", back_populates="topic", order_by="Question.external_id.asc()"
    )

    def __repr__(self):
        return self.name

    def get_short_name(self):
        topic_name = self.name
        regex = r"^[a-zA-z]{1,4}\s*\d{1,4}(\.\d{1,4})?"
        match = re.match(regex, topic_name)

        if match:
            short_name = match.group()
        elif len(topic_name) < 6:
            short_name = topic_name
        else:
            short_name = topic_name[0:6]

        return short_name


class Category(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    questions = relationship(
        "Question", back_populates="category", order_by="Question.external_id.asc()"
    )

    def __repr__(self):
        return self.name


class QuestionType(enum.Enum):
    self_assessed = "self_assessed"
    select_four = "select_four"
    one_decimal = "one_decimal"
    two_decimals = "two_decimals"
    one_of_six = "one_of_six"
    two_of_five = "two_of_five"
    three_to_three = "three_to_three"

    @staticmethod
    def get_values():
        return [el.value for el in QuestionType]


class QuestionUserState(enum.Enum):
    not_tried = 1
    tried_failed = 2
    solved_success = 3


class Question(Model):
    # common
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic", back_populates="questions")
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", back_populates="questions")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
    type = Column(Enum(QuestionType), index=True)
    answered_users = relationship("AssocUserQuestion", back_populates="question")
    assignments = relationship(
        "Assignment",
        secondary=assoc_assignment_question,
        back_populates="assigned_questions",
    )
    video_url = Column(String(), nullable=True)
    cols_common = [
        "external_id",
        "topic",
        "category",
        "description_image",
        "type",
        "video_url",
    ]

    # self_assessed only
    solution_image = Column(ImageColumn(size=(10000, 10000, True)))
    cols_self_assessed = cols_common + ["solution_image"]

    # 1 / 2 decimal(s) only
    value1_upper_limit = Column(Float())
    value1_lower_limit = Column(Float())
    value2_upper_limit = Column(Float())
    value2_lower_limit = Column(Float())
    cols_one_decimal = cols_common + ["value1_upper_limit", "value1_lower_limit"]
    cols_two_decimals = cols_common + [
        "value1_upper_limit",
        "value1_lower_limit",
        "value2_upper_limit",
        "value2_lower_limit",
    ]

    # 1 / 2 of 5 / 6 only
    option1_image = Column(ImageColumn(size=(10000, 10000, True)))
    option1_is_correct = Column(Boolean())
    option2_image = Column(ImageColumn(size=(10000, 10000, True)))
    option2_is_correct = Column(Boolean())
    option3_image = Column(ImageColumn(size=(10000, 10000, True)))
    option3_is_correct = Column(Boolean())
    option4_image = Column(ImageColumn(size=(10000, 10000, True)))
    option4_is_correct = Column(Boolean())
    option5_image = Column(ImageColumn(size=(10000, 10000, True)))
    option5_is_correct = Column(Boolean())
    option6_image = Column(ImageColumn(size=(10000, 10000, True)))
    option6_is_correct = Column(Boolean())
    cols_one_of_six = cols_common + [
        "option1_image",
        "option1_is_correct",
        "option2_image",
        "option2_is_correct",
        "option3_image",
        "option3_is_correct",
        "option4_image",
        "option4_is_correct",
        "option5_image",
        "option5_is_correct",
        "option6_image",
        "option6_is_correct",
    ]
    cols_two_of_five = cols_common + [
        "option1_image",
        "option1_is_correct",
        "option2_image",
        "option2_is_correct",
        "option3_image",
        "option3_is_correct",
        "option4_image",
        "option4_is_correct",
        "option5_image",
        "option5_is_correct",
    ]

    # select 4 only
    selection1_image = Column(ImageColumn(size=(10000, 10000, True)))
    selection1_solution = Column(Enum(Select4Enum))
    selection2_image = Column(ImageColumn(size=(10000, 10000, True)))
    selection2_solution = Column(Enum(Select4Enum))
    selection3_image = Column(ImageColumn(size=(10000, 10000, True)))
    selection3_solution = Column(Enum(Select4Enum))
    selection4_image = Column(ImageColumn(size=(10000, 10000, True)))
    selection4_solution = Column(Enum(Select4Enum))
    cols_select_four = cols_common + [
        "selection1_image",
        "selection1_solution",
        "selection2_image",
        "selection2_solution",
        "selection3_image",
        "selection3_solution",
        "selection4_image",
        "selection4_solution",
        "option1_image",
        "option2_image",
        "option3_image",
        "option4_image",
        "option5_image",
        "option6_image",
    ]

    # 3 to 3 only
    option1a_image = Column(ImageColumn(size=(10000, 10000, True)))
    option1a_is_correct = Column(Boolean())
    option1b_image = Column(ImageColumn(size=(10000, 10000, True)))
    option1b_is_correct = Column(Boolean())
    option1c_image = Column(ImageColumn(size=(10000, 10000, True)))
    option1c_is_correct = Column(Boolean())
    option2a_image = Column(ImageColumn(size=(10000, 10000, True)))
    option2a_is_correct = Column(Boolean())
    option2b_image = Column(ImageColumn(size=(10000, 10000, True)))
    option2b_is_correct = Column(Boolean())
    option2c_image = Column(ImageColumn(size=(10000, 10000, True)))
    option2c_is_correct = Column(Boolean())
    cols_three_to_three = cols_common + [
        "option1a_image",
        "option1a_is_correct",
        "option1b_image",
        "option1b_is_correct",
        "option1c_image",
        "option1c_is_correct",
        "option2a_image",
        "option2a_is_correct",
        "option2b_image",
        "option2b_is_correct",
        "option2c_image",
        "option2c_is_correct",
    ]

    # common
    def __repr__(self):
        topic_short_name = self.topic.get_short_name()

        if self.category:
            extended_info = f"{self.category.name} - "
        else:
            extended_info = ""

        return f"{self.external_id} ({extended_info}{topic_short_name})"

    def state_user(self, user_id):
        tried_but_incorrect = False
        # noinspection PyTypeChecker
        for assoc in self.answered_users:
            if assoc.user_id == user_id:
                if assoc.is_answer_correct:
                    return QuestionUserState.solved_success
                else:
                    tried_but_incorrect = True

        if tried_but_incorrect:
            return QuestionUserState.tried_failed
        else:
            return QuestionUserState.not_tried

    def state(self):
        return self.state_user(g.user.id)

    def description_image_img(self):
        im = ImageManager()
        return Markup(
            '<img src="'
            + im.get_url(self.description_image)
            + '" alt="Photo" class="img-rounded img-responsive question-image">'
        )

    def video_embed_url(self):
        if not self.video_url:
            return None
        url = urlparse(self.video_url.strip())
        if url.hostname in ["www.youtube.com", "youtube.com", "youtu.be"]:
            queries = parse_qs(url.query)
            if url.hostname == "youtu.be":
                video_id = url.path[1:]
            else:
                if queries.get("v", False):
                    video_id = queries["v"][0]
                else:
                    return None
            if queries.get("t", False):
                start_at = queries["t"][0]
                if start_at.endswith("s"):
                    start_at = start_at[:-1]
            else:
                start_at = 0

            video_embed_url = (
                f"https://www.youtube-nocookie.com/embed/{video_id}?start={start_at}"
            )
            return video_embed_url
        return None

    @staticmethod
    def get_option_image(option):
        im = ImageManager()
        return Markup(
            '<img src="'
            + im.get_url(option)
            + '" alt="Photo" class="img-rounded img-responsive option-image">'
        )

    @staticmethod
    def get_option_small_image(option):
        im = ImageManager()
        return Markup(
            '<img src="'
            + im.get_url(option)
            + '" alt="Photo" class="img-rounded img-responsive">'
        )

    # self_assessed only
    def solution_image_img(self):
        im = ImageManager()
        return Markup(
            '<img src="'
            + im.get_url(self.solution_image)
            + '" alt="Photo" class="img-rounded img-responsive">'
        )

    # select_four only
    @staticmethod
    def get_selection_image(selection):
        im = ImageManager()
        return Markup(
            '<img src="'
            + im.get_url(selection)
            + '" alt="Photo" class="img-rounded img-responsive">'
        )


class Assignment(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    learning_group_id = Column(Integer, ForeignKey("learning_group.id"))
    learning_group = relationship("LearningGroup", back_populates="assignments")
    assigned_questions = relationship(
        "Question",
        secondary=assoc_assignment_question,
        back_populates="assignments",
        order_by="Question.external_id.asc()",
    )
    starts_on = Column(DateTime, nullable=False)
    is_due_on = Column(DateTime, nullable=False)

    def __repr__(self):
        return self.name

    @property
    def starts_on_de(self):
        return self.starts_on.strftime("%d.%m.%Y")

    @property
    def is_due_on_de(self):
        return self.is_due_on.strftime("%d.%m.%Y")

    def additional_links(self):
        show_url = url_for("AssignmentModelTeacherView.show", assignment_id=self.id)
        export_url = url_for("AssignmentModelTeacherView.export", assignment_id=self.id)

        return Markup(
            f"""
<div class="btn-group btn-group-xs" style="display: flex;">
    <a href="{show_url}" class="btn btn-sm btn-default" data-toggle="tooltip" rel="tooltip" title="" data-original-title="Auswertung anzeigen">
        <span class="sr-only">Show</span>
        <i class="fa fa-table" aria-hidden="true"></i>
    </a>
    <a href="{export_url}" class="btn btn-sm btn-default" data-toggle="tooltip" rel="tooltip" title="" data-original-title="Auswertung exportieren">
        <span class="sr-only">Export</span>
        <i class="fa fa-download"></i>
    </a>
</div>"""
        )

    def student_link(self):
        url = url_for("AssignmentModelStudentView.show", pk=self.id, _external=True)
        return Markup(f'<a href="{url}">{url}</a>')

    def duplicate(self):
        # noinspection PyArgumentList
        return self.__class__(
            name=f"{self.name} (Duplikat)",
            learning_group_id=self.learning_group_id,
            learning_group=self.learning_group,
            assigned_questions=self.assigned_questions.copy(),
            starts_on=self.starts_on,
            is_due_on=self.is_due_on,
        )


class LearningGroup(Model, AuditMixin):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    users = relationship(
        "ExtendedUser",
        secondary=assoc_user_learning_group,
        back_populates="learning_groups",
        order_by="ExtendedUser.last_name.asc()",
    )
    assignments = relationship(
        "Assignment", back_populates="learning_group", lazy="dynamic"
    )
    join_token = Column(String(255), default=secrets.token_urlsafe())

    def __repr__(self):
        return self.name

    def join_url(self):
        root_url = request.root_url
        join_path = url_for(
            "JoinLearningGroup.join_learning_group",
            group_id=self.id,
            join_token=self.join_token,
        )

        if (root_url[-1] == "/") and (join_path[0] == "/"):
            root_url = root_url[:-1]
        full_url = root_url + join_path
        return Markup(f'<a href="{full_url}">{full_url}</a>')

    def active_assignments(self):
        now = datetime.datetime.now()
        return self.assignments.filter(
            Assignment.starts_on < now, Assignment.is_due_on > now
        ).all()

    def position(self, user):
        return (
            sorted(self.users, key=lambda u: u.correct_questions(), reverse=True).index(
                user
            )
            + 1
        )

    def user_count(self):
        return len(self.users)


class ExtendedUser(User):
    __tablename__ = "ab_user"
    learning_groups = relationship(
        "LearningGroup",
        secondary=assoc_user_learning_group,
        back_populates="users",
        order_by="LearningGroup.name.asc()",
    )
    answered_questions = relationship(
        "AssocUserQuestion",
        back_populates="user",
        lazy="dynamic",
        order_by="AssocUserQuestion.created_on.asc()",
    )
    password_reset_token = Column(String(255))
    password_reset_expiration = Column(DateTime)

    def role_names(self):
        return map(lambda role: role.name, self.roles)

    def tried_questions(self):
        return self.answered_questions.count()

    def correct_questions(self):
        return self.answered_questions.filter_by(is_answer_correct=True).count()

    def correct_percentage(self):
        if self.tried_questions() == 0:
            return "0 %"
        else:
            return f"{int(round(self.correct_questions() / self.tried_questions(), 2) * 100)} %"

    def active_assignments(self):
        # TODO: optimize?
        # noinspection PyTypeChecker
        return reduce(
            operator.concat,
            map(lambda group: group.active_assignments(), self.learning_groups),
            [],
        )

    def answered_by_topic(self):
        def get_topic_name(answer):
            return answer.question.topic.get_short_name()

        answers_by_topic = {}
        correct_count_by_topic = {}
        incorrect_count_by_topic = {}
        # noinspection PyTypeChecker
        for topic_name, question_group in groupby(
            self.answered_questions, get_topic_name
        ):
            answers_by_topic[topic_name] = list(question_group)
            correct_count_by_topic[topic_name] = len(
                list(
                    filter(lambda x: x.is_answer_correct, answers_by_topic[topic_name])
                )
            )
            incorrect_count_by_topic[topic_name] = len(
                list(
                    filter(
                        lambda x: not x.is_answer_correct, answers_by_topic[topic_name]
                    )
                )
            )

        return dict(
            answers=answers_by_topic,
            correct=correct_count_by_topic,
            incorrect=incorrect_count_by_topic,
        )

    def answered_by_week(self):
        def get_week_index(answer):
            min_date = self.answered_questions[0].created_on
            cluster_size = 7
            return (answer.created_on - min_date).days // cluster_size

        answers_by_week = {}
        # noinspection PyTypeChecker
        for week_index, question_group in groupby(
            self.answered_questions, get_week_index
        ):
            answers_by_week[week_index] = list(question_group)
        correct_count_by_week = []
        incorrect_count_by_week = []
        week_indices = []

        if answers_by_week:
            week_indices = list(range(0, max(answers_by_week.keys()) + 1))
            for week_index in week_indices:
                if answers_by_week.get(week_index):
                    correct_count_by_week.append(
                        len(
                            list(
                                filter(
                                    lambda x: x.is_answer_correct,
                                    answers_by_week[week_index],
                                )
                            )
                        )
                    )
                    incorrect_count_by_week.append(
                        len(answers_by_week[week_index])
                        - correct_count_by_week[week_index]
                    )
                else:
                    correct_count_by_week.append(0)
                    incorrect_count_by_week.append(0)
        return dict(
            answers=answers_by_week,
            correct=correct_count_by_week,
            incorrect=incorrect_count_by_week,
            week_indices=week_indices,
        )


class ExtendedRegisterUser(RegisterUser):
    __tablename__ = "ab_register_user"
    role = Column(String(255))  # TODO: should be relation


class AssocUserQuestion(Model):
    __tablename__ = "assoc_user_question"
    id = Column(Integer, Sequence("assoc_user_question_id_seq"), primary_key=True)
    user_id = Column(ForeignKey("ab_user.id"))
    user = relationship("ExtendedUser")
    question_id = Column(ForeignKey("question.id"))
    question = relationship("Question")
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)
    is_answer_correct = Column(Boolean, nullable=False)

    def __repr__(self):
        return (
            f"AssocUserQuestion(id={self.id}, user_id={self.user_id}, user={self.user},"
            f" question_id={self.question_id}, question={self.question},"
            f" created_on={self.created_on}, in_answer_correct={self.is_answer_correct}"
        )
