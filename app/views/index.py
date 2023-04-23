from flask_appbuilder import IndexView, expose

from app.app_factory import db
from app.models.general import Question, Category


class ExtendedIndexView(IndexView):
    index_template = "extended_index.html"

    @expose("/")
    def index(self):
        self.update_redirect()
        question_count = db.session.query(Question).count()
        matura_count = db.session.query(Category).count()
        return self.render_template(
            self.index_template,
            appbuilder=self.appbuilder,
            question_count=question_count,
            matura_count=matura_count,
        )
