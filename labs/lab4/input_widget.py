# class TextInputWidget(Widget):
#     template_name = "text_input_widget.html"
#
#     def __init__(
#         self,
#         label="",
#         input_type="text",
#         input_class="border rounded-md w-full py-2 px-3",
#         placeholder="Placeholder",
#         label_class="block text-sm font-medium text-gray-600",
#         **kwargs
#     ):
#         super().__init__(**kwargs)
#         self.label = label
#         self.input_type = input_type
#         self.input_class = input_class
#         self.placeholder = placeholder
#         self.label_class = label_class
#
#     def get_context(self, name, value, attrs=None, renderer=None):
#         context = super().get_context(name, value, attrs)
#         context["widget"]["label"] = self.label
#         context["widget"]["label_class"] = self.label_class
#         context["widget"]["input_type"] = self.input_type
#         context["widget"]["input_class"] = self.input_class
#         context["widget"]["placeholder"] = self.placeholder
#         return context

from django.forms.utils import flatatt
from django.forms.widgets import Widget


class TextInputWidget(Widget):
    def __init__(
        self,
        label=None,
        input_type="text",
        input_class="border rounded-md w-full py-2 px-3 mb-5",
        placeholder=None,
        label_class="block text-sm font-medium text-gray-600",
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.label = label
        self.input_type = input_type
        self.input_class = input_class
        self.placeholder = placeholder
        self.label_class = label_class

    def render(self, name, value, attrs=None, renderer=None):
        # Define the attributes for the input element
        input_attrs = {
            "type": self.input_type,
            "id": attrs.get("id", ""),
            "name": name,
            "class": self.input_class,
            "placeholder": self.placeholder,
            "value": value,
        }

        # Combine the attributes and generate the HTML
        final_attrs = self.build_attrs(attrs, extra_attrs=input_attrs)

        input_html = f"<input{flatatt(final_attrs)}>"
        return f"{input_html}"