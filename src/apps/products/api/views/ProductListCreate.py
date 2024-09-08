from django.db import transaction

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from src.apps.users.enums.UserRole import UserEnum
from src.common.permissions.roles import IsAuthAndRoles
from .....common.pagination.Pagination import CustomPagination

from ..serializers.ProductSerializer import ProductSerializer
from ..serializers.ImageSerializer import ImageSerializer
from ...models import ProductModel


class ProductListCreate(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = ProductModel.objects.all()
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        elif self.request.method == 'POST':
            return [IsAuthAndRoles([UserEnum.ADMIN, UserEnum.SUPER_ADMIN])]

    def get(self, req):
        #Obteniendo filtros
        search = req.query_params.get('search', '')
        category = req.query_params.get('category', '')
        maxPrice = int(req.query_params.get('maxPrice', 9999999))
        minPrice = int(req.query_params.get('minPrice', 0))
        
        if req.query_params.get('page') is not None:
            if category != '':
                queryset = self.get_queryset().filter(name__icontains=search).filter(category = category)
            else:
                queryset = self.get_queryset().filter(name__icontains=search).filter(price__gte = minPrice).filter(price__lte = maxPrice)
            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                data = self.get_paginated_response(serializer.data)
        else:
            data = ProductSerializer(self.get_queryset(), many=True)
        return Response(
            {
                'msg': "Ok",
                'data': data.data,
                'statusCode': 200
            },
            status.HTTP_200_OK
        )

    # Create
    @transaction.atomic
    def post(self, request):
        sid = transaction.savepoint()
        data = request.data.copy()
        data['name'] = str.capitalize(data['name'])
        archivo = request.FILES.get('file1', None)
        Product_serializer = ProductSerializer(data=data)
        if Product_serializer.is_valid():
            print(request.FILES.items)
            if archivo is None:
                return Response(
                    {
                        'msg': "Error",
                        "statusCode": 400,
                        'errors': {
                            "files": [
                                "product must have at least 1 image"
                            ]
                        }
                    },
                    status.HTTP_400_BAD_REQUEST
                )
            Product_serializer.save()
            for file_name, file_data in request.FILES.items():
                image = {}
                image = {'url': None, 'product': None}
                image['url'] = file_data
                image['product'] = Product_serializer.data['id']
                imageSerializer = ImageSerializer(data=image)
                if imageSerializer.is_valid():
                    imageSerializer.save()
            transaction.savepoint_commit(sid)
            return Response(
                {
                    'status': 201,
                    'msg': 'CREATED',
                    'data': Product_serializer.data
                },
                status=status.HTTP_201_CREATED
            )
        else:
            transaction.savepoint_rollback(sid)
            return Response(
                {
                    'status': 400,
                    'msg': 'Error',
                    'errors': Product_serializer.errors
                },
                status=status.HTTP_400_BAD_REQUEST
            )

