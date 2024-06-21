from src.apps.users.api.serializers.UserSerializer import UserSerializer
from src.apps.users.api.views.UserListCreate import UserCreate
from src.apps.users.enums.UserRole import UserEnum
from src.common.permissions.roles import IsAuthAndRoles


class UserAdminCreate(UserCreate):
    serializer_class = UserSerializer

    def get_permissions(self):
        return [IsAuthAndRoles(UserEnum.SUPER_ADMIN)]

    def post(self, request):
        return self.create_user(request, 'ADMIN')
