from rest_framework import generics, status
from rest_framework.response import Response

from src.apps.users.api.serializers.UserSerializer import UserSerializer
from src.apps.users.enums.UserRole import UserEnum
from src.apps.users.models import UserModel

from src.common.permissions.roles import IsAuthAndRoles


class UserRetrieveDestroy(generics.RetrieveDestroyAPIView):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthAndRoles(UserEnum.SUPER_ADMIN)]
        else:
            return [IsAuthAndRoles([UserEnum.ADMIN, UserEnum.SUPER_ADMIN])]

    def get(self, request, pk=None):
        user = UserModel.objects.filter(id=pk).first()

        if user:
            user_serializer = UserSerializer(user)
            return Response(
                {
                    'msg': 'Ok',
                    'data': user_serializer.data,
                    'statusCode': 200
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'msg': 'User not found',
                'statusCode': 404
            },
            status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, pk=None):
        user = UserModel.objects.filter(id=pk).delete()
        if user:
            return Response(
                {
                    'msg': 'User deleted',
                    'statusCode': 202
                },
                status.HTTP_202_ACCEPTED)
        return Response(
            {
                'msg': 'User not found',
                'statusCode': 400
            },
            status.HTTP_400_BAD_REQUEST)