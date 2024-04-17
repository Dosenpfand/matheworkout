import re

from flask_appbuilder.fieldwidgets import DatePickerWidget
from flask_appbuilder.widgets import RenderTemplateWidget
from markupsafe import Markup
from wtforms.widgets import html_params, Select


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


class SelectWidgetExtended(Select):
    extra_classes = None

    def __init__(self, extra_classes=None, style=None, data_placeholder=None):
        self.extra_classes = extra_classes
        self.style = style
        self.data_placeholder = data_placeholder
        super().__init__()

    def __call__(self, field, **kwargs):
        kwargs["class"] = "form-control"
        if self.extra_classes:
            kwargs["class"] = kwargs["class"] + " " + self.extra_classes
        if self.style:
            kwargs["style"] = self.style
        if self.data_placeholder:
            kwargs["data-placeholder"] = self.data_placeholder
        else:
            kwargs["data-placeholder"] = "Wert auswählen"
        if "name_" in kwargs:
            field.name = kwargs["name_"]
        return super().__call__(field, **kwargs)


class FormMinimalInlineWidget(RenderTemplateWidget):
    template = "form_minimal_inline_widget.html"


class NoSearchWidget:
    def __init__(self, **kwargs):
        return None

    def __call__(self, **kwargs):
        return ""
