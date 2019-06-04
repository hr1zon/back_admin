from rest_framework import serializers

from goods.models import GoodsCategory


class ChannelCategorySerializer(serializers.ModelSerializer):
    '''频道管理商品类型序列化器类'''

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')


class GoodsCategorySimpleSerializer(serializers.ModelSerializer):
    '''spu管理商品类型下拉列表序列化器类'''


    # parent = serializers.StringRelatedField(label='类别名称')
    subs = ChannelCategorySerializer(label='subs',many=True)

    class Meta:
        model = GoodsCategory
        fields = ('id', 'subs', 'name')

