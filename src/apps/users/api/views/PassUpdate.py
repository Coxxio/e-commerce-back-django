from rest_framework import generics, status

from rest_framework.response import Response

from src.apps.users.api.serializers.UserSerializer import UpdatePass
from src.apps.users.models import UserModel


class PassUpdate(generics.UpdateAPIView):
    def patch(self, request):
        id = request.user.id
        user = UserModel.objects.filter(id=id).first()
        if user:
            user_serializer = UpdatePass(user, request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(
                    {
                        'msg': "Password updated",
                        'data': user_serializer.data,
                        'statusCode': 202
                    },
                    status.HTTP_202_ACCEPTED)
        return Response(
            {
                'msg': 'Errors',
                'errors': user_serializer.errors,
                'statusCode': 404
            },
            status.HTTP_404_NOT_FOUND)
