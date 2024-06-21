from django.urls import path

from src.apps.categories.api.views.CategoryRetrieveUpdateDestroy import CategoryRetrieveUpdateDestroy
from src.apps.categories.api.views.CategoryListCreate import CategoryListCreate

urlpatterns = [
    path('', CategoryListCreate.as_view(), name='category_list_create'),
    path('<pk>', CategoryRetrieveUpdateDestroy.as_view(),
         name='category_retrieve_update_destroy')
]
