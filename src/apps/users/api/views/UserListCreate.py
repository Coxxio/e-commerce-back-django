from django.db.models import Q
from django.db import transaction

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .....common.permissions.roles import IsAuthAndRoles
from ...enums.UserRole import UserEnum

from src.apps.users.api.serializers.UserSerializer import UserSerializer, PersonSerializer
from src.apps.users.models import UserModel


class UserList(generics.ListAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.all()


class UserCreate(generics.CreateAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        return self.create_user(request, 'CLIENT')

    @transaction.atomic
    def create_user(self, request, role):
        sid = transaction.savepoint()
        request.data['role'] = role
        userData = request.data
        personData = request.data['person']
        person_serializzer = PersonSerializer(data=personData)
        if person_serializzer.is_valid():
            person_serializzer.save()
        else:
            transaction.savepoint_rollback(sid)
            return Response({
                'msg': 'Hay errores en el registro',
                'errors': person_serializzer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        userData['person'] =  person_serializzer.data['id']
        user_serializer = self.serializer_class(data=userData)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(
                {
                    'statusCode': 201,
                    'data': user_serializer.data,
                    'msg': "CREATED"
                },
                status=status.HTTP_201_CREATED)
        return Response(
            {
                'statusCode': 400,
                'msg': 'errors',
                'errors': user_serializer.errors
            },
            status.HTTP_400_BAD_REQUEST)


class UserUpdate(generics.UpdateAPIView):
    def patch(self, request):
        id = request.user.id
        user = self.get_queryset().filter(id=id).first()
        if 'email' in request.data:
            emailExists = self.get_queryset().filter(
                email=request.data['email']
            ).filter(~Q(id=id)).first()
            if emailExists:
                return Response(
                    {
                        'msg': "this email is already registered with another user",
                        'statusCode': 409
                    },
                    status.HTTP_409_CONFLICT)
        if user:
            user_serializer = UserSerializer(user, request.data, partial=True)
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(
                    {
                        'msg': "User updated",
                        'data': user_serializer.data,
                        'statusCode': 202
                    },
                    status.HTTP_202_ACCEPTED)
        return Response(
            {
                'msg': 'User not found',
                'statusCode': 404
            },
            status.HTTP_404_NOT_FOUND)


class UserListCreate(UserCreate, UserList, UserUpdate):
    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        elif self.request.method == 'PATCH':
            return [IsAuthenticated()]
        else:
            return [IsAuthAndRoles([UserEnum.ADMIN, UserEnum.SUPER_ADMIN])]
