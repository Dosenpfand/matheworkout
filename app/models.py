import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship

class Question2of5(Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(String(1000), nullable=False)
    option1_description = Column(String(150), nullable=False)
    option1_is_correct = Column(Boolean())
    option2_description = Column(String(150), nullable=False)
    option2_is_correct = Column(Boolean())
    option3_description = Column(String(150), nullable=False)
    option3_is_correct = Column(Boolean())
    option4_description = Column(String(150), nullable=False)
    option4_is_correct = Column(Boolean())
    option5_description = Column(String(150), nullable=False)
    option5_is_correct = Column(Boolean())

    def __repr__(self):
        return self.title
