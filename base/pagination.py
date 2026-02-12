from rest_framework.pagination import PageNumberPagination


class BasePagination(PageNumberPagination):
    """
    Base pagination class that can be extended/customized.
    
    Default settings:
    - page_size: 10 items per page
    - max_page_size: 100 items per page
    - Allow client to override page_size via query param
    
    Usage:
        class MyPagination(BasePagination):
            page_size = 20
    """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100
    page_query_param = 'page'



class RidePagination(BasePagination):
    """
    Custom pagination for Ride lists.
    Extends BasePagination with ride-specific settings.
    """
    page_size = 10
    max_page_size = 100
