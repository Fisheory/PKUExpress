from rest_framework.pagination import PageNumberPagination

<<<<<<< HEAD
class TaskPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'size'
    page_query_param = 'page'
    max_page_size = 100
=======

class TaskPaginator(PageNumberPagination):
    page_size = 10
    page_size_query_param = "size"
    page_query_param = "page"
    max_page_size = 100
>>>>>>> ac4d57e3eaba250c9fdd3cb468a030d322ac2ae9
