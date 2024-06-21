from django.urls import path

from src.apps.users.api.views.PassUpdate import PassUpdate
from src.apps.users.api.views.UserAdminCreate import UserAdminCreate
from src.apps.users.api.views.UserDeleteSelf import UserDeleteSelf
from src.apps.users.api.views.UserListCreate import UserListCreate
from src.apps.users.api.views.UserRetrieveDestroy import UserRetrieveDestroy

urlpatterns = [
    path('', UserListCreate.as_view(), name='user_list_create_update'),
    path('admin', UserAdminCreate.as_view(), name='user_admin_create'),
    path('update-password', PassUpdate.as_view(), name='user_update_password'),
    path('delete-me', UserDeleteSelf.as_view(), name='user_delete_self'),
    path('<pk>', UserRetrieveDestroy.as_view(), name='user_retrieve_destroy'),
]
