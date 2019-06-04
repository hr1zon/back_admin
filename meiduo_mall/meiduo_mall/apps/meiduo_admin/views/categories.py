from django.db.models import Q
from rest_framework.decorators import action
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from goods.models import GoodsCategory
from meiduo_admin.serializers.categories import GoodsCategorySimpleSerializer


class GoodsCategorySimpleView(ModelViewSet):
    '''获取商品类型下拉列表'''
    serializer_class = GoodsCategorySimpleSerializer
    # queryset = GoodsCategory.objects.filter(parent=None)

    def get_queryset(self):
        if self.action =='list':
            return GoodsCategory.objects.filter(parent=None)
        elif self.action == 'retrieve':
            pk = self.kwargs['pk']
            category_list = GoodsCategory.objects.filter(pk=pk)
            return category_list

    pagination_class = None