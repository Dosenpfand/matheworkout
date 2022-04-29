from flask_appbuilder import Model
from sqlalchemy import Column, Integer, ForeignKey, String, Sequence, Table, UniqueConstraint, DateTime, Boolean
from sqlalchemy.orm import relationship

assoc_assignment_question = Table('association', Model.metadata,
    Column('assignment_id', ForeignKey('assignment.id'), primary_key=True),
    Column('question_id', ForeignKey('question.id'), primary_key=True)
)
