from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsChannel, GoodsChannelGroup, GoodsCategory
from meiduo_admin.serializers.categories import ChannelCategorySerializer
from meiduo_admin.serializers.channels import ChannelSerializer, ChannelTypeSerializer


class ChannelViewSet(ModelViewSet):
    '''频道表管理'''
    serializer_class = ChannelSerializer
    queryset = GoodsChannel.objects.all()


class ChannelTypesView(ListAPIView):
    serializer_class = ChannelTypeSerializer
    queryset = GoodsChannelGroup.objects.all()
    pagination_class = None


class ChannelCategoryView(ListAPIView):
    serializer_class = ChannelCategorySerializer
    queryset = GoodsCategory.objects.filter(parent=None)
    pagination_class = None