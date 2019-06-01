from rest_framework import serializers

from goods.models import GoodsChannel, GoodsCategory, GoodsChannelGroup


class ChannelSerializer(serializers.ModelSerializer):
    '''频道管理序列化器'''
    group = serializers.StringRelatedField(label='频道组名称')
    category = serializers.StringRelatedField(label='分类名')

    category_id = serializers.IntegerField(label='一级分类ID')
    group_id = serializers.IntegerField(label='频道组ID')

    class Meta:
        model = GoodsChannel
        fields = ('id', 'category', 'category_id', 'group', 'group_id', 'sequence', 'url')

    def validate_category_id(self, value):
        try:
            category = GoodsCategory.objects.get(id=value, parent=None)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('一级分类不存在')

        return value

    def validate_group_id(self, value):
        try:
            group = GoodsChannelGroup.objects.get(id=value)
        except GoodsChannelGroup.DoesNotExist:
            raise serializers.ValidationError('频道组不存在')
        return value


class ChannelTypeSerializer(serializers.ModelSerializer):
    """频道组序列化器类"""

    class Meta:
        model = GoodsChannelGroup
        fields = ('id', 'name')
