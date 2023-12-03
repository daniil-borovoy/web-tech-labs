from django.views.generic import TemplateView

from labs.lab2.menu import menu_tables, menu_queries
from labs.lab5.sale_statistics_view import SalesStatisticsForm


class HomeView(TemplateView):
    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        form = SalesStatisticsForm()
        context = self.get_context_data(**kwargs)
        context.update({"form": form})
        return self.render_to_response(context)


class InfoView(TemplateView):
    template_name = "info.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class Lab1View(TemplateView):
    template_name = "lab1/lab1.html"


class Lab2View(TemplateView):
    template_name = "lab2/lab2.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            context={"tables": menu_tables, "queries": menu_queries}
        )


class Lab3View(TemplateView):
    template_name = "lab3/lab3.html"

    def get(self, request, *args, **kwargs):
        return self.render_to_response(context={"tables": menu_tables})


class LabNotFoundView(TemplateView):
    template_name = "common/lab_not_found.html"


def get_lab_view_by_name(request, lab_name):
    match lab_name:
        case "1":
            return Lab1View.as_view()(request)
        case "2":
            return Lab2View.as_view()(request)
        case "3":
            return Lab3View.as_view()(request)
        case _:
            return LabNotFoundView.as_view()(request)
