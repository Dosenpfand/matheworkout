from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence, Table
from sqlalchemy.orm import relationship, backref
from flask_appbuilder import Model

class ExtendedUser(User):
    __tablename__ = 'ab_user'
    tried_questions = Column(Integer, default=0)
    correct_questions = Column(Integer, default=0)
    learning_group = Column(String)

    def correct_percentage(self):
        if self.tried_questions == 0:
            return 0
        else:
            return int(round(self.correct_questions/self.tried_questions, 2)*100)
