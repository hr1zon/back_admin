from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import Brand
from meiduo_admin.serializers.brands import BrandSerializer, BrandSimpleSerializer


class BrandsViewSet(ModelViewSet):
    '''品牌管理'''
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    serializer_class = BrandSerializer
    queryset = Brand.objects.all()


class BrandSimpleView(ListAPIView):
    lookup_value_regex = '\d+'
    permission_classes = [IsAdminUser]

    serializer_class = BrandSimpleSerializer
    queryset = Brand.objects.all()

    pagination_class = None
