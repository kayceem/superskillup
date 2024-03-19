from rest_framework.pagination import PageNumberPagination


class Pagination(PageNumberPagination):
    page_size = 30
    page_query_param = 'page'
    max_page_size = 100


def paginate(queryset, request):
    paginator = Pagination()
    paginated_queryset = paginator.paginate_queryset(queryset, request)
    page_info = {
        'count': paginator.page.paginator.count,
        'page_number': paginator.page.number,
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
    }
    return paginated_queryset, page_info
