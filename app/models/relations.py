import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, ForeignKey, Sequence, Table, UniqueConstraint, DateTime, Boolean
from sqlalchemy.orm import relationship

assoc_assignment_question = Table('association', Model.metadata,
                                  Column('assignment_id', ForeignKey('assignment.id'), primary_key=True),
                                  Column('question_id', ForeignKey('question.id'), primary_key=True)
                                  )
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
