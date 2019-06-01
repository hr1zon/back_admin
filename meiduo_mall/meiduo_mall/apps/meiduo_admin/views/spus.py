from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet

from goods.models import SPU, SPUSpecification
from meiduo_admin.serializers.spus import SPUSimpleSerializer, SPUSpecSerializer


class SPUSimpleView(ListAPIView):
    ''' 获取SPU表数据'''
    serializer_class =SPUSimpleSerializer
    queryset = SPU.objects.all()

    pagination_class = None


class SPUSpecView(ListAPIView):
    serializer_class = SPUSpecSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        spuspec = SPUSpecification.objects.filter(spu_id=pk)
        return spuspec

    pagination_class = None
