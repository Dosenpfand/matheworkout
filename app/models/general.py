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
from flask_appbuilder.security.sqla.models import User
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
import sqlalchemy
from sqlalchemy.orm import relationship, joinedload

from app.utils.iter import groupby_unsorted


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


class Select2Enum(enum.Enum):
    A = "A"
    B = "B"
    C = "C"
    D = "D"

    @staticmethod
    def get_values():
        return [el.value for el in Select2Enum]


class SchoolType(enum.Enum):
    ahs = "AHS"
    bhs = "BHS"


assoc_user_learning_group = Table(
    "assoc_user_learning_group",
    Model.metadata,
    Column("user_id", ForeignKey("ab_user.id"), primary_key=True),
    Column("learning_group_id", ForeignKey("learning_group.id"), primary_key=True),
)
assoc_user_achievement = Table(
    "assoc_user_achievement",
    Model.metadata,
    Column("user_id", ForeignKey("ab_user.id"), primary_key=True),
    Column("achievement_id", ForeignKey("achievement.id"), primary_key=True),
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
    school_type = Column(Enum(SchoolType), nullable=False)

    def __repr__(self):
        return self.name

    def get_short_name(self) -> str:
        topic_name = self.name
        regex = r"^([a-zA-z]{1,4}\s*)?\d{1,4}(\.\d{1,4})?"
        match = re.match(regex, topic_name)

        if match:
            short_name = match.group()
        elif len(topic_name) < 6:
            short_name = topic_name
        else:
            short_name = topic_name[0:6]

        return short_name

    def count(self) -> int:
        return len(self.questions)


class Category(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    questions = relationship(
        "Question", back_populates="category", order_by="Question.external_id.asc()"
    )
    school_type = Column(Enum(SchoolType), nullable=False)

    def __repr__(self):
        return self.name


class QuestionType(enum.Enum):
    self_assessed = "self_assessed"
    select_four = "select_four"
    select_two = "select_two"
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
    external_id = Column(String, nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic", back_populates="questions")
    category_id = Column(Integer, ForeignKey("category.id"), nullable=False)
    category = relationship("Category", back_populates="questions")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
    type = Column(Enum(QuestionType), index=True)
    answered_users = relationship(
        "AssocUserQuestion",
        back_populates="question",
        lazy="dynamic",
        cascade="all, delete",
    )
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

    # 1 / 2 of 5 / 6 and select 2 / 4 only
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

    # select 2 / 4 only
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
    cols_select_two = cols_common + [
        "selection1_image",
        "selection1_solution",
        "selection2_image",
        "selection2_solution",
        "option1_image",
        "option2_image",
        "option3_image",
        "option4_image",
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
        category = f"{self.category.name} - "
        return f"{self.external_id} ({category}{topic_short_name})"

    def as_export_dict(self):
        return {
            "topic": self.topic.get_short_name(),
            "category": self.category.name,
            "id": self.external_id,
        }

    def get_solution(self):
        if self.type == QuestionType.self_assessed:
            return Markup(self.solution_image_print())
        elif self.type == QuestionType.select_four:
            return Markup(
                f"1{self.selection1_solution}, "
                f"2{self.selection2_solution}, "
                f"3{self.selection3_solution}, "
                f"4{self.selection4_solution}, "
            )
        elif self.type == QuestionType.select_two:
            return Markup(
                f"1{self.selection1_solution}, " f"2{self.selection2_solution}, "
            )
        elif self.type == QuestionType.one_decimal:
            return Markup(
                f"<div>{self.value1_lower_limit} ≤ Ergebnis 1 ≤ {self.value1_upper_limit}</div>"
            )
        elif self.type == QuestionType.two_decimals:
            return Markup(
                f"<div>{self.value1_lower_limit} ≤ Ergebnis 1 ≤ {self.value1_upper_limit} | "
                f"{self.value2_lower_limit} ≤ Ergebnis 2 ≤ {self.value2_upper_limit}</div>"
            )
        elif self.type in [
            QuestionType.one_of_six,
            QuestionType.two_of_five,
        ]:
            correct_list = []
            if self.option1_is_correct:
                correct_list.append("1")
            if self.option2_is_correct:
                correct_list.append("2")
            if self.option3_is_correct:
                correct_list.append("3")
            if self.option4_is_correct:
                correct_list.append("4")
            if self.option5_is_correct:
                correct_list.append("5")
            if self.option6_is_correct:
                correct_list.append("6")
            return Markup("Richtig: {}".format(", ".join(correct_list)))
        elif self.type == QuestionType.three_to_three:
            correct_list = []
            if self.option1a_is_correct:
                correct_list.append("1A")
            if self.option1b_is_correct:
                correct_list.append("1B")
            if self.option1c_is_correct:
                correct_list.append("1C")
            if self.option2a_is_correct:
                correct_list.append("2A")
            if self.option2b_is_correct:
                correct_list.append("2B")
            if self.option2c_is_correct:
                correct_list.append("2C")
            return Markup("Richtig: {}".format(", ".join(correct_list)))

    def state_user(self, user_id):
        tried_but_incorrect = False

        answers = self.answered_users.filter_by(user_id=user_id).all()

        if not answers:
            return QuestionUserState.not_tried

        if any([answer.is_answer_correct for answer in answers]):
            return QuestionUserState.solved_success
        else:
            return QuestionUserState.tried_failed

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

    def video_link_url(self):
        if (not self.video_url) or self.video_embed_url():
            return None
        return self.video_url.strip()

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
            + '" alt="Photo" class="img-rounded img-responsive option-small-image">'
        )

    # self_assessed only
    def solution_image_img(self):
        im = ImageManager()
        return Markup(
            '<img src="'
            + im.get_url(self.solution_image)
            + '" alt="Photo" class="img-rounded img-responsive">'
        )

    def solution_image_print(self):
        im = ImageManager()
        return Markup(
            '<img src="'
            + im.get_url(self.solution_image)
            + '" alt="Photo" style="max-height: 20em" class="img-rounded img-responsive">'
        )

    # select_four / select_two only
    @staticmethod
    def get_selection_image(selection):
        im = ImageManager()
        return Markup(
            '<img src="'
            + im.get_url(selection)
            + '" alt="Photo" class="img-rounded img-responsive selection-image">'
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
        representation = f"{self.name}"
        if self.learning_group:
            representation += f" ({self.learning_group.name})"
        return representation

    @property
    def starts_on_de(self):
        return self.starts_on.strftime("%d.%m.%Y")

    @property
    def is_due_on_de(self):
        return self.is_due_on.strftime("%d.%m.%Y")

    def additional_links(self):
        show_url = url_for("AssignmentModelEvaluationView.show", assignment_id=self.id)
        export_url = url_for(
            "AssignmentModelEvaluationView.export", assignment_id=self.id
        )

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
        lazy="dynamic",
        secondary=assoc_user_learning_group,
        back_populates="learning_groups",
        order_by="ExtendedUser.last_name.asc()",
    )
    assignments = relationship(
        "Assignment",
        back_populates="learning_group",
        lazy="dynamic",
        cascade="all, delete",
    )
    join_token = Column(String(255), default=secrets.token_urlsafe())

    def __repr__(self):
        return self.name

    def as_export_dict(self):
        return {"name": self.name}

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

    def ranking(self):
        users_ranked = (
            self.users.outerjoin(
                AssocUserQuestion,
                sqlalchemy.and_(
                    AssocUserQuestion.user_id == ExtendedUser.id,
                    AssocUserQuestion.is_answer_correct == True,
                ),
            )
            .order_by(None)
            .group_by(ExtendedUser.id)
            .order_by(sqlalchemy.func.count(AssocUserQuestion.id).desc())
            .all()
        )
        # NOTE: Currently does not consider tied positions
        ranking = {user: position + 1 for position, user in enumerate(users_ranked)}
        return ranking

    def position(self, user):
        return self.ranking()[user]

    def user_count(self):
        return self.users.count()


class ExtendedUser(User):
    __tablename__ = "ab_user"
    learning_groups = relationship(
        "LearningGroup",
        secondary=assoc_user_learning_group,
        back_populates="users",
        order_by="LearningGroup.name.asc()",
    )
    created_learning_groups = relationship(
        "LearningGroup",
        back_populates="created_by",
        foreign_keys="LearningGroup.created_by_fk",
        cascade="all, delete",
    )
    changed_learning_groups = relationship(
        "LearningGroup",
        back_populates="changed_by",
        foreign_keys="LearningGroup.changed_by_fk",
        cascade="all, delete",
    )
    answered_questions = relationship(
        "AssocUserQuestion",
        back_populates="user",
        lazy="dynamic",
        order_by="AssocUserQuestion.created_on.asc()",
        cascade="all, delete",
    )
    achievements = relationship(
        "Achievement",
        secondary=assoc_user_achievement,
        back_populates="users",
    )
    password_reset_token = Column(String(255))
    password_reset_expiration = Column(DateTime)
    email_confirmation_token = Column(String(255))
    account_delete_token = Column(String(255))
    account_delete_expiration = Column(DateTime)
    school_type = Column(Enum(SchoolType), nullable=False)

    def as_export_dict(self):
        return {
            "common": {
                "first_name": self.first_name,
                "last_name": self.last_name,
                "username": self.username,
                "school_type": self.school_type.value,
            },
            "learning_groups": [lq.as_export_dict() for lq in self.learning_groups],
            "created_learning_groups": [
                lg.as_export_dict() for lg in self.created_learning_groups
            ],
            "answered_questions": [
                aq.as_export_dict() for aq in self.answered_questions
            ],
            "achievements": [
                achievement.as_export_dict() for achievement in self.achievements
            ],
        }

    def role_names(self):
        return map(lambda role: role.name, self.roles)

    def tried_questions(self):
        return self.answered_questions.count()

    def correct_questions(self):
        return self.answered_questions.filter_by(is_answer_correct=True).count()

    def correct_percentage_int(self):
        if self.tried_questions() == 0:
            return 0
        return int(round(self.correct_questions() / self.tried_questions(), 2) * 100)

    def correct_percentage(self):
        return f"{self.correct_percentage_int()} %"

    def active_assignments(self):
        # noinspection PyTypeChecker
        return reduce(
            operator.concat,
            map(lambda group: group.active_assignments(), self.learning_groups),
            [],
        )

    def answered_by_topic(self):
        correct_count_by_topic = {}
        incorrect_count_by_topic = {}

        # NOTE: group_by directly in query is somehow much slower
        answered_questions = self.answered_questions.options(
            joinedload(AssocUserQuestion.question).joinedload(Question.topic)
        ).all()

        answer_groups = groupby_unsorted(
            answered_questions, lambda answer: answer.question.topic.get_short_name()
        )

        # noinspection PyTypeChecker
        counts = {}
        for topic_name, answer_group in answer_groups:
            answers_by_topic = list(answer_group)
            correct_count_by_topic = len(
                [answer for answer in answers_by_topic if answer.is_answer_correct]
            )
            incorrect_count_by_topic = len(
                [answer for answer in answers_by_topic if not answer.is_answer_correct]
            )
            counts[topic_name] = dict(
                correct=correct_count_by_topic,
                incorrect=incorrect_count_by_topic,
            )

        return dict(
            sorted(
                counts.items(),
                key=lambda item: item[1]["correct"] + item[1]["incorrect"],
                reverse=True,
            )
        )

    def answered_by_week(self):
        def get_week_index(answer):
            cluster_size = 7
            return (answer.created_on - min_date).days // cluster_size

        min_date = self.answered_questions[0].created_on
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


class Achievement(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False, unique=True, index=True)
    title = Column(String(150), nullable=False)
    description = Column(String(150), nullable=False)
    users = relationship(
        "ExtendedUser",
        secondary=assoc_user_achievement,
        back_populates="achievements",
    )

    def as_export_dict(self):
        return {
            "name": self.name,
            "title": self.title,
            "description": self.description,
        }


class AssocUserQuestion(Model):
    __tablename__ = "assoc_user_question"
    id = Column(Integer, Sequence("assoc_user_question_id_seq"), primary_key=True)
    user_id = Column(ForeignKey("ab_user.id"), nullable=False)
    user = relationship("ExtendedUser")
    question_id = Column(ForeignKey("question.id"), nullable=False)
    question = relationship("Question")
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)
    is_answer_correct = Column(Boolean, nullable=False)

    def __repr__(self):
        return (
            f"AssocUserQuestion(id={self.id},"
            f" user_id={self.user_id},"
            f" question_id={self.question_id},"
            f" created_on={self.created_on},"
            f" in_answer_correct={self.is_answer_correct}"
        )

    def as_export_dict(self):
        return {
            "question": self.question.as_export_dict(),
            "created_on": self.created_on,
            "is_answer_correct": self.is_answer_correct,
        }
