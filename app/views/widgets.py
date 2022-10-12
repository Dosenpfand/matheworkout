from flask_appbuilder.widgets import RenderTemplateWidget


class ExtendedEditWidget(RenderTemplateWidget):
    template = "extended_form.html"


class ExtendedListWidget(RenderTemplateWidget):
    template = "extended_list.html"


class ExtendedListNoButtonsWidget(RenderTemplateWidget):
    template = "extended_list_no_buttons.html"


class ExtendedShowWidget(RenderTemplateWidget):
    template = "extended_show.html"
