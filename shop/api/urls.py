from django.urls import path
from .views import (CategoryListView,CategoryDetailView,
                        ProductListView,ProductDetailView,
                        ProductAdd,ProductRemove,Cart,
                        AddDiscount,CheckoutView,VerifyView
                        )
urlpatterns = [
    path("categories/",CategoryListView.as_view(),name="categories"),
    path("category/<slug:slug>/",CategoryDetailView.as_view(),name="category"),
    path("cart/",Cart.as_view(),name="cart"),
    path("checkout/",CheckoutView.as_view(),name="checkout"),
    path("verify/",VerifyView.as_view(),name="verify"),
    path("discount/",AddDiscount.as_view(),name="add-discount"),
    path("products/",ProductListView.as_view(),name="products"),
    path("product/<slug:slug>/",ProductDetailView.as_view(),name="product"),
    path("product/<int:id>/add/",ProductAdd.as_view(),name="product-add"),
    path("product/<int:id>/remove/",ProductRemove.as_view(),name="product-remove"),
]
