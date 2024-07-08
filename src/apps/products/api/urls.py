from django.urls import path

# from src.apps.category.api.views.CategoryRetrieveUpdateDestroy import CategoryRetrieveUpdateDestroy
from src.apps.products.api.views.ProductListCreate import ProductListCreate

urlpatterns = [
    path('', ProductListCreate.as_view(), name='products_list_create'),
    # path('<pk>', CategoryRetrieveUpdateDestroy.as_view(),
    #      name='category_retrieve_update_destroy')
]
