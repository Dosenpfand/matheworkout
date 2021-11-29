import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

class Question2of5(Model):
    id = Column(Integer, primary_key=True)
    title = Column(String(150), nullable=False)
    description = Column(String(1000), nullable=False)
    task = Column(String(150), nullable=False)
    picture_path = Column(String(150), nullable=True)
    option_correct1 = Column(String(150), nullable=False)
    option_correct2 = Column(String(150), nullable=False)
    option_incorrect1 = Column(String(150), nullable=False)
    option_incorrect2 = Column(String(150), nullable=False)
    option_incorrect3 = Column(String(150), nullable=False)

    def __repr__(self):
        return self.title
