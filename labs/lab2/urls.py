from django.urls import path, include
from . import views

queries = [
    path('suppliers-in-city/', views.suppliers_in_city, name='suppliers_in_city'),
    path('products-sold-today/', views.products_sold_in_day, name='products_sold_in_day'),
    path('revenue-in-month/', views.revenue_in_month, name='revenue_in_month'),
    path('most-popular-product/', views.most_popular_product, name='most_popular_product'),
    path('supplier-shop-products/', views.supplier_shop_products, name='supplier_shop_products'),
]

urlpatterns = [
    path('tables/<str:table_name>/', views.table_page, name='table'),
    path('queries/', include(queries)),
]

