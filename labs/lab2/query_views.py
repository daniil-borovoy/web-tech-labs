from datetime import date

from dateutil import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, F, Count
from django.utils.dateparse import parse_date
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from labs.models import Product, Sale, Supplier


@method_decorator(login_required, name="dispatch")
class SuppliersInCityQueryView(TemplateView):
    template_name = "common/model_data.html"

    def get(self, request, *args, **kwargs):
        value = (
            request.GET.get("filter_value")
            if request.GET.get("filter_value") is not None
            else "Москва"
        )
        suppliers = Supplier.objects.filter(address__icontains=value, deleted=False)
        fields = [
            f for f in Supplier._meta.fields if f.name != "id" and f.name != "deleted"
        ]
        return self.render_to_response(
            {
                "model_name": f"Перечень поставщиков, расположенных по адресу в г. {value}",
                "fields": fields,
                "page_obj": suppliers,
                "hide_filter_value": True,
                "is_read_only": True,
                "home_link": "/labs/2/",
                "hide_pagination": True,
            },
        )


@method_decorator(login_required, name="dispatch")
class ProductsSoldInDayQueryView(TemplateView):
    template_name = "common/model_data.html"

    def get(self, request, *args, **kwargs):
        # Get today's date
        today = date.today()
        fields = [
            f for f in Product._meta.fields if f.name != "id" and f.name != "deleted"
        ]

        value = (
            parse_date(request.GET.get("filter_value"))
            if request.GET.get("filter_value") is not None
            and len(request.GET.get("filter_value")) > 0
            else today
        )

        # Query products sold today by filtering the Sale model
        products_sold = Product.objects.filter(sale__date=value, deleted=False)

        return self.render_to_response(
            {
                "model_name": "Cписок товаров, проданных за сегодняшний день",
                "fields": fields,
                "page_obj": products_sold,
                "input_type": "date",
                "input_value": value.strftime("%Y-%m-%d"),
                "hide_filter_value": True,
                "is_read_only": True,
                "home_link": "/labs/2/",
                "hide_pagination": True,
            },
        )


@method_decorator(login_required, name="dispatch")
class RevenueInMonthQueryView(TemplateView):
    template_name = "lab2/queries/query_3.html"

    def get(self, request, *args, **kwargs):
        february_month_number = 2
        current_year = date.today().year
        year = (
            int(request.GET.get("year"))
            if request.GET.get("year") is not None
            else current_year
        )
        month = (
            int(request.GET.get("month"))
            if request.GET.get("month") is not None
            else february_month_number
        )

        start_date = date(year, month, 1)
        end_date = start_date + relativedelta.relativedelta(months=1)

        sales_in_february = Sale.objects.filter(
            product__sale__date__range=[start_date, end_date], deleted=False
        ).annotate(revenue=Sum(F("count") * F("retail_price")))

        total_revenue = sales_in_february[0].revenue if len(sales_in_february) else 0

        title = f"Выручка за {month} месяц, {year} года"

        return self.render_to_response(
            {
                "title": title,
                "value": total_revenue,
                "initial_year": year,
                "initial_month": month,
                "home_link": "/labs/2/",
            },
        )


@method_decorator(login_required, name="dispatch")
class MostPopularProductQueryView(TemplateView):
    template_name = "lab2/queries/one_value_display.html"

    def get(self, request, *args, **kwargs):
        most_popular = (
            Product.objects.annotate(sales_count=Count("sale"))
            .order_by("-sales_count")
            .first()
        )

        return self.render_to_response(
            {
                "title": "Самый популярный товар",
                "value": most_popular,
                "home_link": "/labs/2/",
            },
        )


@method_decorator(login_required, name="dispatch")
class SupplierShopProductsQueryView(TemplateView):
    template_name = "lab2/queries/query_5.html"

    def get(self, request, *args, **kwargs):
        selected_supplier = (
            request.GET.get("filter_field")
            if request.GET.get("filter_field") is not None
            else "Mi SHOP"
        )

        suppliers = Supplier.objects.all()
        ascending = (
            bool(request.GET.get("ascending"))
            if request.GET.get("ascending") is not None
            else True
        )

        mi_shop_products_data = Product.objects.filter(
            supply__supplier__name=selected_supplier, deleted=False
        ).order_by("-price")
        fields = [
            f for f in Product._meta.fields if f.name != "id" and f.name != "deleted"
        ]

        return self.render_to_response(
            {
                "title": f"Список товаров, поставляемый {selected_supplier}, отсортированный от самого дорогого до самого дешевого",
                "fields": fields,
                "data": mi_shop_products_data,
                "suppliers": suppliers,
                "selected_supplier": selected_supplier,
                "ascending": ascending,
                "home_link": "/labs/2/",
            },
        )
