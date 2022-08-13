import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, ForeignKey, Sequence, Table, DateTime, Boolean
from sqlalchemy.orm import relationship
from app.security.models import ExtendedUser # noqa

assoc_assignment_question = Table('association', Model.metadata,
                                  Column('assignment_id', ForeignKey('assignment.id'), primary_key=True),
                                  Column('question_id', ForeignKey('question.id'), primary_key=True)
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
