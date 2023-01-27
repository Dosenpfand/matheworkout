from flask_appbuilder.fieldwidgets import DatePickerWidget
from flask_appbuilder.widgets import RenderTemplateWidget


class ExtendedEditWidget(RenderTemplateWidget):
    template = "extended_form.html"


class ExtendedListWidget(RenderTemplateWidget):
    template = "extended_list.html"


class ExtendedListNoButtonsWidget(RenderTemplateWidget):
    template = "extended_list_no_buttons.html"


class ExtendedShowWidget(RenderTemplateWidget):
    template = "extended_show.html"


class ListWithDeleteRelationshipWidget(RenderTemplateWidget):
    template = "list_with_delete_relationship.html"


class RegisterFormWidget(RenderTemplateWidget):
    template = "form_register.html"


class DatePickerWidgetDe(DatePickerWidget):
    data_template = (
        '<div class="input-group date appbuilder_date" id="datepicker">'
        '<span class="input-group-addon"><i class="fa fa-calendar cursor-hand"></i>'
        "</span>"
        '<input class="form-control" data-format="dd.MM.yyyy" %(text)s />'
        "</div>"
    )
