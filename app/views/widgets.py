import re

from flask_appbuilder.fieldwidgets import DatePickerWidget, Select2AJAXWidget
from flask_appbuilder.widgets import RenderTemplateWidget
from markupsafe import Markup
from wtforms.widgets import html_params
from re import search


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

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("name", field.name)
        if not field.data:
            field.data = ""
        match = re.search(
            r"^(?P<year>\d+)-(?P<month>\d+)-(?P<day>\d+)( \d+:\d+:\d+)?$",
            str(field.data),
        )
        if match:
            field.data = (
                f"{match.group('day')}.{match.group('month')}.{match.group('year')}"
            )
        template = self.data_template

        return Markup(
            template % {"text": html_params(type="text", value=field.data, **kwargs)}
        )


class Select2AJAXExtendedWidget(Select2AJAXWidget):
    data_template = "<input %(text)s />"

    def __init__(self, endpoint, extra_classes=None, style=None, placeholder=None):
        self.endpoint = endpoint
        self.extra_classes = extra_classes
        self.placeholder = placeholder
        self.style = style or "max-width:100%"

    def __call__(self, field, **kwargs):
        kwargs.setdefault("id", field.id)
        kwargs.setdefault("name", field.name)
        kwargs.setdefault("endpoint", self.endpoint)
        kwargs.setdefault("style", self.style)
        kwargs.setdefault("placeholder", self.placeholder)
        input_classes = "input-group my_select2_ajax"
        if self.extra_classes:
            input_classes = input_classes + " " + self.extra_classes
        kwargs.setdefault("class", input_classes)
        if not field.data:
            field.data = ""
        template = self.data_template

        return Markup(
            template % {"text": html_params(type="text", value=field.data, **kwargs)}
        )


class FormMinimalInlineWidget(RenderTemplateWidget):
    template = "form_minimal_inline_widget.html"
