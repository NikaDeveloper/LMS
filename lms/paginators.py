from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'  # Параметр запроса для выбора кол-ва элементов
    max_page_size = 100
