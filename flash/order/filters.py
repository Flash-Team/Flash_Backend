from rest_framework import filters


class DeliveredFilter(filters.BaseFilterBackend):
    """
    Filter orders as delivered and not
    """
    def filter_queryset(self, request, queryset, view):
        delivered = request.query_params.get('delivered')

        if delivered is not None:
            delivered.capitalize()

        if delivered in ('True', 'False'):
            queryset = queryset.filter(delivered=delivered)

        return queryset
