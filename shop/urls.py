from django.urls import path
from django.views.generic import TemplateView
from .views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateSuccessView,
    ProductUpdateView,
    ProductDeleteView,
    CategoryListView,
    CategoryCreateView,
    CategoryDetailView,
    OrderCreateView, 
    PaymentCreateView,
    BasketView, 
    AddToBasketView, 
    RemoveFromBasketView,
    OrderSuccessView,
    RegisterView,
    LoginView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategoryUpdateSuccessView,
    CategoryDeleteSuccessView
    
)

urlpatterns = [
    path('', ProductListView.as_view(), name='product_list'),
    path('products/new/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/edit/', ProductUpdateView.as_view(), name='product_update'),
  path('product/<int:pk>/delete/', ProductDeleteView.as_view(), name='product-delete'), 
  path('product/deleted/', TemplateView.as_view(template_name='product/product_deleted.html'), name='product-deleted'),
  path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/new/', CategoryCreateView.as_view(), name='category_create'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category_detail'),
    path('category/create/', CategoryCreateView.as_view(), name='category-create'),
    path('create_order/', OrderCreateView.as_view(), name='create_order'),
    path('create_payment/', PaymentCreateView.as_view(), name='create_payment'),
    path('basket/', BasketView.as_view(), name='basket'),
    path('add_to_basket/<int:product_id>/', AddToBasketView.as_view(), name='add_to_basket'),
    path('remove_from_basket/<int:product_id>/', RemoveFromBasketView.as_view(), name='remove_from_basket'),
    path('order_success/', OrderSuccessView.as_view(), name='order_success'),
    path('login/', LoginView.as_view(), name='login'),
 path('register/', RegisterView.as_view(), name='register'),
 path('categories/new/', CategoryCreateView.as_view(), name='category_create'), 
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category_update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
    path('categories/update/success/', CategoryUpdateSuccessView.as_view(), name='category_update_success'),
    path('categories/delete/success/', CategoryDeleteSuccessView.as_view(), name='category_delete_success') ,
    path('product/update/success/', ProductUpdateSuccessView.as_view(), name='product_update_success')   
    
]
