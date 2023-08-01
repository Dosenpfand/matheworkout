from flask_appbuilder import IndexView, expose

from app import db
from app.models.general import Question, Category, SchoolType, Topic


class ExtendedIndexView(IndexView):
    index_template = "extended_index.html"

    @expose("/")
    def index(self):
        self.update_redirect()
        question_count_ahs = (
            db.session.query(Question)
            .join(Topic)
            .filter(Topic.school_type == SchoolType.ahs)
            .count()
        )
        print(SchoolType.ahs)
        print(db.session.query(Question).first())
        question_count_bhs = (
            db.session.query(Question)
            .join(Topic)
            .filter(Topic.school_type == SchoolType.bhs)
            .count()
        )
        matura_count_ahs = (
            db.session.query(Category).filter_by(school_type=SchoolType.ahs).count()
        )
        matura_count_bhs = (
            db.session.query(Category).filter_by(school_type=SchoolType.bhs).count()
        )
        return self.render_template(
            self.index_template,
            appbuilder=self.appbuilder,
            question_count_ahs=question_count_ahs,
            question_count_bhs=question_count_bhs,
            matura_count_ahs=matura_count_ahs,
            matura_count_bhs=matura_count_bhs,
            title="Willkommen",
        )
