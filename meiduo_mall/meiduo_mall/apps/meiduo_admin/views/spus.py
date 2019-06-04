from django.conf import settings
from django.contrib.sessions.backends import file
from rest_framework.exceptions import APIException
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from goods.models import SPU, SPUSpecification
from meiduo_admin.serializers.spus import SPUSimpleSerializer, SPUSpecSerializer, SPUSerializer
from utils.fdfs.storage import FDFSStorage


class SPUSimpleView(ListAPIView):
    ''' 获取简易SPU表数据'''
    serializer_class =SPUSimpleSerializer
    queryset = SPU.objects.all()

    pagination_class = None


class SPUSpecView(ListAPIView):
    '''获取SPU规格信息'''
    serializer_class = SPUSpecSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        spuspec = SPUSpecification.objects.filter(spu_id=pk)
        return spuspec

    pagination_class = None


class SPUViewSet(ModelViewSet):
    '''获取SPU数据表详情'''
    serializer_class = SPUSerializer
    queryset = SPU.objects.all()
    lookup_value_regex = '\d+'


class SPUImagesView(APIView):
    '''富文本插入图片'''
    def post(self,request):
        data = request.data

        fdfs = FDFSStorage()
        file = data['image']
        print(file)
        try:
            file_id = fdfs.save(file.name, file)
        except Exception:
            raise APIException('上传失败')
        image_id = settings.FDFS_URL + file_id

        return Response({'img_url':image_id})
