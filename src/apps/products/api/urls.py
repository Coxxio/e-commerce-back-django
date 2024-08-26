from django.urls import path

# from src.apps.category.api.views.CategoryRetrieveUpdateDestroy import CategoryRetrieveUpdateDestroy
from src.apps.products.api.views.ProductListCreate import ProductListCreate
from src.apps.products.api.views.ProductRetrieveUpdateDelete import ProductsRetrieveUpdateDelete

urlpatterns = [
    path('', ProductListCreate.as_view(), name='products_list_create'),
    path('<id>', ProductsRetrieveUpdateDelete.as_view(),
         name='products_retrieve_update_destroy')
]
