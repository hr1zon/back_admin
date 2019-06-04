from rest_framework import serializers
from rest_framework.exceptions import APIException

from goods.models import Brand
from utils.fdfs.storage import FDFSStorage


class BrandSerializer(serializers.ModelSerializer):
    '''品牌管理序列化器类'''
    class Meta:
        model = Brand
        exclude = ('create_time', 'update_time')

    def create(self, validated_data):
        # 获取上传文件对象
        file = validated_data['logo']

        brand = validated_data['id']
        # 上传图片到FDFS系统
        fdfs = FDFSStorage()
        try:
            file_id = fdfs.save(file.name, file)
        except Exception:
            raise APIException('上传失败')
        # 保存上传记录
        brand_logo = Brand.objects.create(
            name = validated_data['name'],
            logo = file_id,
            first_letter = validated_data['first_letter']
        )
        if not brand.logo:
            brand.logo = brand_logo.logo.url
            brand.save()

        return brand_logo

    def update(self, instance, validated_data):
        # 获取上传文件对象
        file = validated_data['logo']

        # 获取brand名称
        name = validated_data['name']

        # 获取首字母
        first_letter = validated_data['first_letter']

        # 上传图片到fdfs系统
        fdfs = FDFSStorage()
        try:
            file_id = fdfs.save(file.name, file)
        except Exception:
            # 上传文件失败
            raise APIException('上传文件失败')

        # 修改SKU图片数据
        instance.name = name
        instance.logo = file_id
        instance.first_letter = first_letter
        instance.save()

        return instance


class BrandSimpleSerializer(serializers.ModelSerializer):
    '''获取品牌下拉列表序列化器类'''
    class Meta:
        model = Brand
        fields = ('id', 'name')