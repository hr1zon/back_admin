from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.generics import UpdateAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from meiduo_admin.serializers.orders import OrderListSerializer, OrderDetailSerializer, OrderStatusSerializer
from orders.models import OrderInfo


class OrdersViewSet(UpdateModelMixin, ReadOnlyModelViewSet):
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'retrieve':
            return OrderDetailSerializer
        else:
            return OrderStatusSerializer
    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')

        if keyword:
            order = OrderInfo.objects.filter(Q(skus__sku__name__contains=keyword) | Q(order_id=keyword))
        else:
            order = OrderInfo.objects.all()

        return order

    @action(methods=['put'], detail=True)
    def status(self, request, pk):
    #     '''修改订单状态'''
    #     order = self.get_object()
    #
    #     serializer = OrderStatusSerializer(order, request.data)
    #
    #     serializer.is_valid(raise_exception=True)
    #
    #     serializer.save()

        # return Response(serializer.data)
        return self.update(request, pk)