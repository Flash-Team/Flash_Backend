from rest_framework import filters

from flash.order.models import Order


class OrderFilter(filters.BaseFilterBackend):
    """
    Filter orders for clients and couriers,
    also filters as delivered and not
    """
    def filter_queryset(self, request, queryset, view):
        return Order.get_orders(request.user, request.query_params.get('delivered'))
