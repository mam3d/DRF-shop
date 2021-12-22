from django.urls import path
from .views import (
    CategoryListView,
    CategoryDetailView,
    ProductListView,
    ProductDetailView,
    AddProductToCart,
    AddDiscount,
    RemoveProductFromCart,
    Cart,
    CheckoutView,
    )

urlpatterns = [
    path("categories/",CategoryListView.as_view(),name="categories"),
    path("category/<slug:slug>/",CategoryDetailView.as_view(),name="category"),
    path("cart/",Cart.as_view(),name="cart"),
    path("cart/add/",AddProductToCart.as_view(),name="cart_add"),
    path("cart/remove/",RemoveProductFromCart.as_view(),name="cart_remove"),
    path("cart/discount/",AddDiscount.as_view(),name="add_discount"),
    path("checkout/",CheckoutView.as_view(),name="checkout"),
    path("products/",ProductListView.as_view(),name="products"),
    path("product/<slug:slug>/",ProductDetailView.as_view(),name="product"),
]
