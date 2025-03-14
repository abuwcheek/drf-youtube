from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination
from rest_framework.response import Response


class MyPageNumberPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'  
    max_page_size = 100  
