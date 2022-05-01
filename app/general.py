from flask_appbuilder import IndexView


class ExtendedIndexView(IndexView):
    index_template = 'extended_index.html'
