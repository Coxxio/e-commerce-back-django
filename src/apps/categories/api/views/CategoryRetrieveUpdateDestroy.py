from django.db.models import Q

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from src.apps.users.enums.UserRole import UserEnum
from src.common.permissions.roles import IsAuthAndRoles

from ..serializers.CategorySerializer import CategorySerializer
from ...models import CategoryModel


class CategoryRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer

    def get_queryset(self):
        return self.get_serializer().Meta.model.objects.filter()

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'PUT' or self.request.method == 'DELETE':
            return [IsAuthAndRoles([UserEnum.ADMIN, UserEnum.SUPER_ADMIN])]

    def get(self, request, pk=None):
        category = CategoryModel.objects.filter(id=pk).first()

        if category:
            category_serializer = CategorySerializer(category)
            return Response(
                {
                    'msg': 'Ok',
                    'data': category_serializer.data,
                    'statusCode': 200
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                'msg': 'category not found',
                'statusCode': 404
            },
            status.HTTP_404_NOT_FOUND)
        

    def put(self, request, pk=None):
        data = request.data.copy()
        category = self.get_queryset().filter(id=pk).first()

        if category:
            if 'img' in data:
                category.img.delete()
            category_serializer = CategorySerializer(
                category, data, partial=True)
            if category_serializer.is_valid():
                category_serializer.save()
                return Response(
                    {
                        'msg': "category updated",
                        'data': category_serializer.data,
                        'statusCode': 202
                    },
                    status.HTTP_202_ACCEPTED)
            else:
                return Response(
                    {
                        'msg': "error",
                        'errors': category_serializer.errors,
                        'statusCode': 400
                    },
                    status.HTTP_400_BAD_REQUEST)
        return Response(
            {
                'msg': 'category not found',
                'statusCode': 404
            },
            status.HTTP_404_NOT_FOUND)
        

    def delete(self, request, pk=None):
        category = CategoryModel.objects.filter(id=pk).first()
        if category:
            category.img.delete()
            category.delete()
            return Response(
                {
                    'msg': 'category deleted',
                    'statusCode': 202
                },
                status.HTTP_202_ACCEPTED)
        return Response(
            {
                'msg': 'category not found',
                'statusCode': 400
            },
            status.HTTP_400_BAD_REQUEST)

