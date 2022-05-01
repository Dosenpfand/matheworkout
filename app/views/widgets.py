from flask_appbuilder.widgets import RenderTemplateWidget


class ExtendedEditWidget(RenderTemplateWidget):
    template = 'extended_form.html'
