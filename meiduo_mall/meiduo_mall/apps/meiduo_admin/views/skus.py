from django.db.models import Q
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SKUImage, SKU, GoodsCategory
from meiduo_admin.serializers.skus import SKUImageSerializer, SKUSimpleSerializer, SKUSerializer, \
    CategorySimpleSerializer


class SKUImageViewSet(ModelViewSet):
    '''图片表数据'''
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    serializer_class = SKUImageSerializer
    queryset = SKUImage.objects.all()


class SKUSimpleView(ListAPIView):
    '''获取sku商品数据'''
    serializer_class = SKUSimpleSerializer
    queryset = SKU.objects.all()

    pagination_class = None


class SKUViewSet(ModelViewSet):
    '''获取sku数据'''
    lookup_value_regex = '\d+'

    serializer_class = SKUSerializer
    def get_queryset(self):

        keyword = self.request.query_params.get('keyword')

        if keyword:
            sku = SKU.objects.filter(Q(name__contains=keyword) | Q(caption__contains=keyword))

        else:
            sku = SKU.objects.all()

        return sku


class SKUCategoriesView(ListAPIView):
    '''获取第三级分类数据'''
    serializer_class = CategorySimpleSerializer

    def get_queryset(self):

        categories = GoodsCategory.objects.filter(subs=None)

        return categories

    pagination_class = None


