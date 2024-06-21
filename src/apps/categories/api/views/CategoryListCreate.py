from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from src.apps.users.enums.UserRole import UserEnum
from src.common.permissions.roles import IsAuthAndRoles

from ..serializers.CategorySerializer import CategorySerializer
from ...models import CategoryModel


class CategoryListCreate(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = CategoryModel.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthAndRoles([UserEnum.ADMIN, UserEnum.SUPER_ADMIN])]

    def get(self, req):
        categories = self.get_queryset()
        serializer = CategorySerializer(categories, many=True)
        return Response(
            {
                'msg': "Ok",
                'data': serializer.data,
                'statusCode': 200
            },
            status.HTTP_200_OK
        )

    # Create
    def post(self, request):
        data = request.data.copy()
        data['name'] = str.capitalize(request.data['name'])
        category_serializer = CategorySerializer(data=data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(
                {
                    'status': 201,
                    'msg': 'CREATED',
                    'data': category_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {
                    'status': 400,
                    'msg': "error",
                    "errors": category_serializer.errors
                }, status.HTTP_400_BAD_REQUEST)
