import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean, Float, Enum
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import ImageColumn
from flask_appbuilder.filemanager import ImageManager
from flask import Markup, url_for
import enum

class Select4Enum(enum.Enum):
    A = 'A'
    B = 'B'
    C = 'C'
    D = 'D'
    E = 'E'
    F = 'F'

class Topic(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    def __repr__(self):
        return self.name

class QuestionSelfAssessed(Model):
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
    solution_image = Column(ImageColumn(size=(10000, 10000, True)))

    def description_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.description_image) +\
            '" alt="Photo" class="img-rounded img-responsive">')

    def solution_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.solution_image) +\
            '" alt="Photo" class="img-rounded img-responsive">')

class Question2of5(Model):
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
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

    def get_option_image(self, option):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(option) +\
            '" alt="Photo" class="img-rounded img-responsive" style="min-width:100%;max-width:4096px;">')

    def description_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.description_image) +\
            '" alt="Photo" class="img-rounded img-responsive">')



    def __repr__(self):
        return self.title

class Question1of6(Model):
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
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

    def get_option_image(self, option):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(option) +\
            '" alt="Photo" class="img-rounded img-responsive" style="min-width:100%;max-width:4096px;">')

    def description_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.description_image) +\
            '" alt="Photo" class="img-rounded img-responsive">')

    def __repr__(self):
        return self.title

class Question3to3(Model):
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
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

    def get_option_image(self, option):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(option) +\
            '" alt="Photo" class="img-rounded img-responsive" style="min-width:100%;max-width:4096px;">')

    def description_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.description_image) +\
            '" alt="Photo" class="img-rounded img-responsive">')



    def __repr__(self):
        return self.title

class Question2Decimals(Model):
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
    value1_upper_limit = Column(Float())
    value1_lower_limit = Column(Float())
    value2_upper_limit = Column(Float())
    value2_lower_limit = Column(Float())

    def description_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.description_image) +\
            '" alt="Photo" class="img-rounded img-responsive">')



    def __repr__(self):
        return self.title

class Question1Decimal(Model):
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
    value_upper_limit = Column(Float())
    value_lower_limit = Column(Float())

    def description_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.description_image) +\
            '" alt="Photo" class="img-rounded img-responsive">')



    def __repr__(self):
        return self.title


class QuestionSelect4(Model):
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
    selection1_image = Column(ImageColumn(size=(10000, 10000, True)))
    selection1_solution = Column(Enum(Select4Enum))
    selection2_image = Column(ImageColumn(size=(10000, 10000, True)))
    selection2_solution = Column(Enum(Select4Enum))
    selection3_image = Column(ImageColumn(size=(10000, 10000, True)))
    selection3_solution = Column(Enum(Select4Enum))
    selection4_image = Column(ImageColumn(size=(10000, 10000, True)))
    selection4_solution = Column(Enum(Select4Enum))
    option1_image = Column(ImageColumn(size=(10000, 10000, True)))
    option2_image = Column(ImageColumn(size=(10000, 10000, True)))
    option3_image = Column(ImageColumn(size=(10000, 10000, True)))
    option4_image = Column(ImageColumn(size=(10000, 10000, True)))
    option5_image = Column(ImageColumn(size=(10000, 10000, True)))
    option6_image = Column(ImageColumn(size=(10000, 10000, True)))


    def get_option_image(self, option):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(option) +\
            '" alt="Photo" class="img-rounded img-responsive" style="max-width:4096px;">')

    def get_selection_image(self, selection):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(selection) +\
            '" alt="Photo" class="img-rounded img-responsive" style="min-width:100%;max-width:4096px;">')

    def description_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.description_image) +\
            '" alt="Photo" class="img-rounded img-responsive">')



    def __repr__(self):
        return self.title
