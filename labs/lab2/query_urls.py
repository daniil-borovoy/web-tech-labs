from django.urls import path

from labs.lab2.query_views import (
    SuppliersInCityQueryView,
    ProductsSoldInDayQueryView,
    RevenueInMonthQueryView,
    MostPopularProductQueryView,
    SupplierShopProductsQueryView,
)

queries = [
    path(
        "suppliers-in-city/",
        SuppliersInCityQueryView.as_view(),
        name="suppliers_in_city",
    ),
    path(
        "products-sold-today/",
        ProductsSoldInDayQueryView.as_view(),
        name="products_sold_in_day",
    ),
    path(
        "revenue-in-month/", RevenueInMonthQueryView.as_view(), name="revenue_in_month"
    ),
    path(
        "most-popular-product/",
        MostPopularProductQueryView.as_view(),
        name="most_popular_product",
    ),
    path(
        "supplier-shop-products/",
        SupplierShopProductsQueryView.as_view(),
        name="supplier_shop_products",
    ),
]
