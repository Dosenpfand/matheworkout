from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.models.relations import assoc_user_topics


class ExtendedUser(User):
    __tablename__ = 'ab_user'
    tried_questions = Column(Integer, default=0)
    correct_questions = Column(Integer, default=0)
    active_topics = relationship("Topic", secondary=assoc_user_topics)
    learning_group_id = Column(Integer, ForeignKey("learning_group.id"))
    learning_group = relationship("LearningGroup", back_populates="users")

    answered_questions = relationship("AssocUserQuestion", back_populates="user")

    def correct_percentage(self):
        if self.tried_questions == 0:
            return 0
        else:
            return int(round(self.correct_questions / self.tried_questions, 2) * 100)
