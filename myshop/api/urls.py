from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import (CategoryList,
                    ProductList,
                    AddToCart,
                    UpdateCart,
                    RemoveFromCart,
                    CartDetails,
                    ClearCart)


router = DefaultRouter()
router.register(r'cart', CartDetails, basename='cart')


urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('products/', ProductList.as_view(), name='product-list'),
    path('add-to-cart/', AddToCart.as_view(), name='add_to_cart'),
    path('update-cart/<int:cart_id>/', UpdateCart.as_view(), name='update_cart'),
    path('remove-from-cart/<int:cart_id>/', RemoveFromCart.as_view(), name='remove_from_cart'),
    path('clear-cart/', ClearCart.as_view(), name='clear_cart'),
]
