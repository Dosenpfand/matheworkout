import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Date, ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import ImageColumn
from flask_appbuilder.filemanager import ImageManager
from flask import Markup, url_for

class Topic(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    def __repr__(self):
        return self.name

class QuestionSelfAssessed(Model):
    id = Column(Integer, primary_key=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
    solution_image = Column(ImageColumn(size=(10000, 10000, True)))

    def description_image_img(self):
        im = ImageManager()
        if self.description_image:
            return Markup('<a href="' + url_for('QuestionSelfAssessedModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url(self.description_image) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('QuestionSelfAssessedModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

    def solution_image_img(self):
        im = ImageManager()
        if self.solution_image:
            return Markup('<a href="' + url_for('QuestionSelfAssessedModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url(self.solution_image) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('QuestionSelfAssessedModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

class Question2of5(Model):
    id = Column(Integer, primary_key=True)
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
        if option:
            return Markup('<a href="' + url_for('Question2of5ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url(option) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('Question2of5ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

    def description_image_img(self):
        im = ImageManager()
        if self.description_image:
            return Markup('<a href="' + url_for('Question2of5ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url(self.description_image) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('Question2of5ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')



    def __repr__(self):
        return self.title

class Question1of6(Model):
    id = Column(Integer, primary_key=True)
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
        if option:
            return Markup('<a href="' + url_for('Question1of6ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url(option) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('Question1of6ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

    def description_image_img(self):
        im = ImageManager()
        if self.description_image:
            return Markup('<a href="' + url_for('Question1of6ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url(self.description_image) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('Question1of6ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')



    def __repr__(self):
        return self.title

class Question3to3(Model):
    id = Column(Integer, primary_key=True)
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
        if option:
            return Markup('<a href="' + url_for('Question3to3ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url(option) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('Question3to3ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')

    def description_image_img(self):
        im = ImageManager()
        if self.description_image:
            return Markup('<a href="' + url_for('Question3to3ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="' + im.get_url(self.description_image) +\
              '" alt="Photo" class="img-rounded img-responsive"></a>')
        else:
            return Markup('<a href="' + url_for('Question3to3ModelView.show',pk=str(self.id)) +\
             '" class="thumbnail"><img src="//:0" alt="Photo" class="img-responsive"></a>')



    def __repr__(self):
        return self.title
