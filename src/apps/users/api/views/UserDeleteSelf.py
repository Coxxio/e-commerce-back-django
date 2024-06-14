from rest_framework import generics, status
from rest_framework.response import Response

from src.apps.users.models import UserModel


class UserDeleteSelf(generics.DestroyAPIView):

    def delete(self, request):
        id = request.user.id
        user = UserModel.objects.filter(id=id).delete()
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
