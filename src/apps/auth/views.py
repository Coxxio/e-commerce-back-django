from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from ..users.models import UserModel
from ..users.api.serializers.UserSerializer import UserSerializer


class Login(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '')
        password = request.data.get('password', '')
        try:
            user = authenticate(
                email=email,
                password=password
            )
            if user:
                login_serializer = self.serializer_class(data=request.data)
                if login_serializer.is_valid():
                    user_serializer = UserSerializer(user)
                    return Response({
                        'msg': 'Session started',
                        'data': {
                            'token': login_serializer.validated_data.get('access'),
                            'user': user_serializer.data
                        },
                        'statusCode': 201
                    }, status.HTTP_201_CREATED)
                else:
                    return Response({'msg': 'User or password incorrect'}, status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'msg': 'User not found'}, status.HTTP_404_NOT_FOUND)
        except AttributeError:
            return Response({'msg': 'User not found'}, status.HTTP_404_NOT_FOUND)


class Logout(GenericAPIView):
    def post(self, request, *args, **kwargs):
        id = request.user.id
        user = UserModel.objects.filter(id=id).first()
        if user:
            return Response({'msg': 'Sesion start'}, status.HTTP_202_ACCEPTED)
        return Response({'msg': 'User not found'}, status.HTTP_400_BAD_REQUEST)


class AuthMe(GenericAPIView):
    def get(self, request, *args, **kwargs):
        id = request.user.id
        user = UserModel.objects.filter(id=id).first()
        if user:
            user_serializer = UserSerializer(user)
            return Response({'msg': 'Sesion start', 'data': user_serializer.data, 'statusCode': 200}, status=status.HTTP_200_OK)
        return Response({'msg': 'User not found.'}, status.HTTP_404_NOT_FOUND)
