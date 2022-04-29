from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence, Table, UniqueConstraint, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from flask_appbuilder import Model
import datetime
from .models import Topic, Question
from .models_assoc import assoc_assignment_question

assoc_user_topics = Table(
    "ab_user_topic",
    Model.metadata,
    Column("id", Integer, Sequence("ab_user_topic_id_seq"), primary_key=True),
    Column("user_id", Integer, ForeignKey("ab_user.id")),
    Column("topic_id", Integer, ForeignKey("topic.id")),
    UniqueConstraint("user_id", "topic_id"),
)

class AssocUserQuestion(Model):
    __tablename__ = 'assoc_user_question'
    id = Column(Integer, Sequence("assoc_user_question_id_seq"), primary_key=True)
    user_id = Column(ForeignKey('ab_user.id'))
    question_id = Column(ForeignKey('question.id'))
    user = relationship("ExtendedUser")
    question = relationship("Question")
    created_on = Column(DateTime, default=datetime.datetime.now, nullable=False)
    is_answer_correct = Column(Boolean, nullable=False)

class LearningGroup(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    def __repr__(self):
        return self.name

class Assignment(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    learning_group_id = Column(Integer, ForeignKey("learning_group.id"))
    learning_group = relationship("LearningGroup")
    # TODO: back_populates or backref needed?
    assigned_questions = relationship("Question", secondary=assoc_assignment_question)
    starts_on = Column(DateTime, nullable=False)
    is_due_on = Column(DateTime, nullable=False)

    def __repr__(self):
        return self.name

class ExtendedUser(User):
    __tablename__ = 'ab_user'
    tried_questions = Column(Integer, default=0)
    correct_questions = Column(Integer, default=0)
    active_topics = relationship("Topic", secondary=assoc_user_topics)
    learning_group_id = Column(Integer, ForeignKey("learning_group.id"))
    learning_group = relationship("LearningGroup")

    answered_questions = relationship("AssocUserQuestion", back_populates="user")

    def correct_percentage(self):
        if self.tried_questions == 0:
            return 0
        else:
            return int(round(self.correct_questions/self.tried_questions, 2)*100)
