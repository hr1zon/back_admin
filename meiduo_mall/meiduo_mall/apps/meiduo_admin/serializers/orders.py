from rest_framework import serializers

from goods.models import SKU
from orders.models import OrderInfo, OrderGoods


class OrderListSerializer(serializers.ModelSerializer):
    '''订单信息列表序列化器类'''

    create_time = serializers.DateTimeField(label='下单时间', format='%Y-%m-%d %H:%M:%S')
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'create_time')

class SKUSerializer(serializers.ModelSerializer):
    '''sku数据序列化器类'''
    class Meta:
        model = SKU
        fields = ('name', 'default_image')

class OrderGoodSerializer(serializers.ModelSerializer):
    '''订单商品序列化器类'''
    sku = SKUSerializer(label='sku数据')
    class Meta:
        model = OrderGoods
        fields = ('count', 'price', 'sku')

class OrderDetailSerializer(serializers.ModelSerializer):
    '''订单详情序列化器类'''
    user = serializers.StringRelatedField(label='下单用户')
    skus = OrderGoodSerializer(label='订单商品信息', many=True)
    class Meta:
        model = OrderInfo
        exclude = ('address', 'update_time')


class OrderStatusSerializer(serializers.ModelSerializer):
    '''订单状态序列化器类'''
    class Meta:
        model = OrderInfo
        fields = ('order_id', 'status')
        read_only_fields = ('order_id',)

    def validate_status(self, value):

        if value not in [1, 2, 3, 4, 5, 6]:
            raise serializers.ValidationError('订单状态错误')

        return value
