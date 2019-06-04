from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from goods.models import SPUSpecification
from meiduo_admin.serializers.specs import SpecSerializer


class SpecsViewSet(ModelViewSet):
    '''规格管理'''
    permission_classes = [IsAdminUser]
    lookup_value_regex = '\d+'
    serializer_class = SpecSerializer
    queryset = SPUSpecification.objects.all()
