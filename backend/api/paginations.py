from rest_framework.pagination import PageNumberPagination


class MyCustomPagination(PageNumberPagination):
    page_size_query_param = 'limit'
