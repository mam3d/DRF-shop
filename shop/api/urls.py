from django.urls import path
from .views import (CategoryListView,CategoryDetailView,
                        ProductListView,ProductDetailView,
                        ProductAdd,
                        )
urlpatterns = [
    path("categories/",CategoryListView.as_view(),name="categories"),
    path("category/<slug:slug>/",CategoryDetailView.as_view(),name="category"),
    path("products/",ProductListView.as_view(),name="products"),
    path("product/<slug:slug>/",ProductDetailView.as_view(),name="product"),
    path("product/<int:id>/add/",ProductAdd.as_view(),name="product-add"),
]
