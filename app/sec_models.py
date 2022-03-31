from flask_appbuilder.security.sqla.models import User
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence, Table, UniqueConstraint
from sqlalchemy.orm import relationship, backref
from flask_appbuilder import Model
from .models import Topic

assoc_user_topics = Table(
    "ab_user_topic",
    Model.metadata,
    Column("id", Integer, Sequence("ab_user_role_id_seq"), primary_key=True),
    Column("user_id", Integer, ForeignKey("ab_user.id")),
    Column("topic_id", Integer, ForeignKey("topic.id")),
    UniqueConstraint("user_id", "topic_id"),
)

class ExtendedUser(User):
    __tablename__ = 'ab_user'
    tried_questions = Column(Integer, default=0)
    correct_questions = Column(Integer, default=0)
    learning_group = Column(String)
    active_topics = relationship("Topic", secondary=assoc_user_topics)

    def correct_percentage(self):
        if self.tried_questions == 0:
            return 0
        else:
            return int(round(self.correct_questions/self.tried_questions, 2)*100)
