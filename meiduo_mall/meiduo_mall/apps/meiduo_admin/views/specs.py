from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SPUSpecification, SpecificationOption
from meiduo_admin.serializers.specs import SpecSerializer, SpecsOptionSerializer


class SpecsViewSet(ModelViewSet):
    '''规格管理'''
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    serializer_class = SpecSerializer
    queryset = SPUSpecification.objects.all()


class SpecOptionViewSet(ModelViewSet):
    '''规格选项管理'''
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    serializer_class = SpecsOptionSerializer
    queryset = SpecificationOption.objects.all()


