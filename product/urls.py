from django.urls import path
from . import views

# include app
app_name = 'product'

urlpatterns = [
    
    
    path('detail/<int:product_id>', views.productdetail, name = 'product_detail'),
    path('addproduct/', views.add_product, name = 'add_product'),
    path('userproducts/',views.user_products, name = 'user_products'),
    path('update/<slug:product_slug>', views.update_product, name = 'update_product'),
    path('list/', views.productlist, name = 'product_list'),
    path('category/<slug:category_slug>', views.productlist, name = 'product_list_category'),
    path('brand/<slug:brand_slug>', views.productlist, name = 'product_list_brand'),
    path('delete/<slug:product_slug>', views.deleteProduct, name = 'delete_product'),
]
