from rest_framework import pagination
from rest_framework.response import Response

class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'perPage'
    max_page_size = 50
    page_query_param = 'page'
    
    
    def get_paginated_response(self, data):
        return Response({
            'total_items': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data
        })

    