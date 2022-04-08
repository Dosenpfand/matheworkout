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

    def get_values():
        return [el.value for el in Select4Enum]


class Topic(Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)

    def __repr__(self):
        return self.name


class QuestionType(enum.Enum):
    self_assessed = 'self_assessed'
    select_four = 'select_four'
    one_decimal = 'one_decimal'
    two_decimals = 'two_decimals'
    one_of_six = 'one_of_six'
    two_of_five = 'two_of_five'
    three_to_three = 'three_to_three'

    def get_values():
        return [el.value for el in QuestionType]


class Question(Model):
    # common
    id = Column(Integer, primary_key=True)
    external_id = Column(Integer, nullable=False, index=True)
    topic_id = Column(Integer, ForeignKey("topic.id"), nullable=False)
    topic = relationship("Topic")
    description_image = Column(ImageColumn(size=(10000, 10000, True)))
    type = Column(Enum(QuestionType), index=True)
    cols_common = ['external_id', 'topic', 'description_image', 'type']
    answered_users = relationship("AssocUserQuestion", back_populates="question")

    # self_assessed only
    solution_image = Column(ImageColumn(size=(10000, 10000, True)))
    cols_self_assessed = cols_common + ['solution_image']

    # 1 / 2 decimal(s) only
    value1_upper_limit = Column(Float())
    value1_lower_limit = Column(Float())
    value2_upper_limit = Column(Float())
    value2_lower_limit = Column(Float())
    cols_one_decimal = cols_common + \
        ['value1_upper_limit', 'value1_lower_limit']
    cols_two_decimals = cols_common + ['value1_upper_limit', 'value1_lower_limit',
                                       'value2_upper_limit', 'value2_lower_limit']

    # 1 / 2 of 5 / 6 only
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
    cols_one_of_six = cols_common + ['option1_image', 'option1_is_correct',
                                     'option2_image', 'option2_is_correct',
                                     'option3_image', 'option3_is_correct',
                                     'option4_image', 'option4_is_correct',
                                     'option5_image', 'option5_is_correct',
                                     'option6_image', 'option6_is_correct',
                                     ]
    cols_two_of_five = cols_common + ['option1_image', 'option1_is_correct',
                                      'option2_image', 'option2_is_correct',
                                      'option3_image', 'option3_is_correct',
                                      'option4_image', 'option4_is_correct',
                                      'option5_image', 'option5_is_correct',
                                      ]

    # select 4 only
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
    cols_select_four = cols_common + ['selection1_image', 'selection1_solution',
                                      'selection2_image', 'selection2_solution',
                                      'selection3_image', 'selection3_solution',
                                      'selection4_image', 'selection4_solution',
                                      'option1_image',
                                      'option2_image',
                                      'option3_image',
                                      'option4_image',
                                      'option5_image',
                                      'option6_image']

    # 3 to 3 only
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
    cols_three_to_three = cols_common + ['option1a_image', 'option1a_is_correct',
                                         'option1b_image', 'option1b_is_correct',
                                         'option1c_image', 'option1c_is_correct',
                                         'option2a_image', 'option2a_is_correct',
                                         'option2b_image', 'option2b_is_correct',
                                         'option2c_image', 'option2c_is_correct',
                                         ]

    # common
    def description_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.description_image) +
                      '" alt="Photo" class="img-rounded img-responsive">')

    def __repr__(self):
        return f'<Question: {self.id=}, {self.external_id=}'

    def get_option_image(self, option):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(option) +
                      '" alt="Photo" class="img-rounded img-responsive" style="max-width:4096px;">')

    # self_assessed only
    def solution_image_img(self):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(self.solution_image) +
                      '" alt="Photo" class="img-rounded img-responsive">')

    # select_four only
    def get_selection_image(self, selection):
        im = ImageManager()
        return Markup('<img src="' + im.get_url(selection) +
                      '" alt="Photo" class="img-rounded img-responsive" style="min-width:100%;max-width:4096px;">')
