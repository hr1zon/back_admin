from rest_framework import serializers

from goods.models import GoodsCategory


class ChannelCategorySerializer(serializers.ModelSerializer):


    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')