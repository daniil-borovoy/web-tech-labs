from django import forms
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Coalesce, Cast
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

from labs.models import Sale


class SalesStatisticsWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        sales_data = Sale.objects.values("product__name").annotate(
            total_sales=Coalesce(
                Sum(Cast(F("count"), output_field=FloatField()) * F("retail_price")),
                0.0,
            )
        )

        output = ["<ul>"]
        for sale in sales_data:
            output.append(f'<li>{sale["product__name"]}: {sale["total_sales"]}</li>')
        output.append("</ul>")

        return mark_safe("\n".join(output))


class SalesStatisticsForm(forms.Form):
    sales_statistics = forms.CharField(
        widget=SalesStatisticsWidget(),
        label=_("Sales statistics"),
    )
