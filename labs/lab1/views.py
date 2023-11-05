from django.forms import Form
from django.views.generic import FormView

from labs.models import Product, Supplier


class ProductFormView(FormView):
    template_name = "lab1/product_form.html"
    form_class = Form

    def post(self, request, *args, **kwargs):
        product = Product(
            name=request.POST["name"],
            receipt_date=request.POST["receipt_date"],
            count=request.POST["count"],
            price=request.POST["price"],
        )

        return self.render_to_response(context={"product": product})


class SupplierFormView(FormView):
    template_name = "lab1/supplier_form.html"
    form_class = Form

    def post(self, request, *args, **kwargs):
        supplier = Supplier(
            name=request.POST["name"],
            who_to_contact=request.POST["who_to_contact"],
            address=request.POST["who_to_contact"],
            phone=request.POST["phone"],
        )
        return self.render_to_response(context={"supplier": supplier})
