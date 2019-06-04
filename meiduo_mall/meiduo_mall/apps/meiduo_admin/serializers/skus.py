from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException

from goods.models import SKUImage, SKU, SKUSpecification, GoodsCategory, SPU, SpecificationOption
from meiduo_mall.utils.fdfs.storage import FDFSStorage


class SKUImageSerializer(serializers.ModelSerializer):
    '''图片表序列化器类'''

    sku = serializers.StringRelatedField(label='sku商品名称')
    sku_id = serializers.IntegerField(label='sku商品id')

    class Meta:
        model = SKUImage
        fields = ('id', 'sku', 'sku_id', 'image')

    def validate_sku_id(self, value):

        try:
            sku = SKU.objects.get(id=value)
        except SKU.DoesNotExist:
            raise serializers.ValidationError('sku商品不存在')

        return sku

    def create(self, validated_data):
        # 获取上传文件对象
        file = validated_data['image']
        # 获取sku对象
        sku = validated_data['sku_id']
        # 上传图片到FDFS系统
        fdfs = FDFSStorage()
        try:
            file_id = fdfs.save(file.name, file)
        except Exception:
            raise APIException('上传失败')
        # 保存上传记录
        sku_image = SKUImage.objects.create(
            sku=sku,
            image=file_id
        )

        # sku 商品默认图片设置
        if not sku.default_image:
            sku.default_image = sku_image.image.url
            sku.save()

        return sku_image

    def update(self, instance, validated_data):
        # 获取上传文件对象
        file = validated_data['image']

        # 获取sku对象
        sku = validated_data['sku_id']

        # 上传图片到fdfs系统
        fdfs = FDFSStorage()
        try:
            file_id = fdfs.save(file.name, file)
        except Exception:
            # 上传文件失败
            raise APIException('上传文件失败')

        # 修改SKU图片数据
        instance.sku = sku
        instance.image = file_id
        instance.save()

        return instance


class SKUSimpleSerializer(serializers.ModelSerializer):
    '''sku商品数据序列化器类'''

    class Meta:
        model = SKU
        fields = ('id', 'name')


class SKUSpecSerializer(serializers.ModelSerializer):
    '''sku商品具体规格序列化器类'''
    spec_id = serializers.IntegerField(label='规格id')
    option_id = serializers.IntegerField(label='选项id')

    class Meta:
        model = SKUSpecification
        fields = ('spec_id', 'option_id')


class CategorySimpleSerializer(serializers.ModelSerializer):
    '''商品第三级分类序列化器类'''

    class Meta:
        model = GoodsCategory
        fields = ('id', 'name')


class SKUSerializer(serializers.ModelSerializer):
    '''sku商品表'''
    spu = serializers.StringRelatedField(label='spu名称')
    category = serializers.StringRelatedField(label='三级分类名称')
    specs = SKUSpecSerializer(label='商品规格信息', many=True)

    spu_id = serializers.IntegerField(label='spu id')
    category_id = serializers.IntegerField(label='第三级分类ID')

    class Meta:
        model = SKU
        exclude = ('default_image', 'create_time', 'update_time')

        # 补充校验：
        # 分类是否存在
        # spu是否存在
        # 分类id和spu的第三级分类id是否一致
        # spu的规格数量和传递的规格数据是否一致
        # spu的规格内容和传递的规格内容是否一致[11， 12， 13] [11， 12， 13]
        # 传递每个规格选项在spu对应规格选项中是否存在
    def validate(self, attrs):
        # 分类是否存在
        category_id = attrs['category_id']
        try:
            category = GoodsCategory.objects.get(id=category_id)
        except GoodsCategory.DoesNotExist:
            raise serializers.ValidationError('商品类别不存在')

        # spu是否存在
        spu_id = attrs['spu_id']
        try:
            spu = SPU.objects.get(id=spu_id)
        except SPU.DoesNotExist:
            raise serializers.ValidationError('SPU商品不存在')

        # 分类id和spu的第三级分类id是否一致
        if spu.category3_id != category_id:
            raise serializers.ValidationError('商品分类错误')

        # spu的规格数量和传递的规格数据是否一致
        specs = attrs['specs']

        spu_specs = spu.specs.all()
        spu_specs_count = spu_specs.count()

        if spu_specs_count != len(specs):
            raise serializers.ValidationError('规格数量错误')

        # spu的规格内容和传递的规格内容是否一致[11， 12， 13] [11， 12， 13]
        spu_specs_ids = [spec.id for spec in spu_specs]
        specs_ids = [spec.get('spec_id') for spec in specs]
        spu_specs_ids.sort()
        specs_ids.sort()
        if spu_specs_ids != specs_ids:
            raise serializers.ValidationError('规格内容错误')

        # 传递每个规格选项在spu对应规格选项中是否存在
        for spec in specs:
            spec_id = spec.get('spec_id')
            option_id = spec.get('option_id')

        options = SpecificationOption.objects.filter(spec_id=spec_id)
        option_ids = [option.id for option in options]
        if option_id not in option_ids:
            raise serializers.ValidationError('规格选项信息错误')

        return attrs

    def create(self, validated_data):

        specs = validated_data.pop('specs')

        with transaction.atomic():
            sku = super().create(validated_data)

        for spec in specs:
            SKUSpecification.objects.create(
                sku = sku,
                spec_id = spec.get('spec_id'),
                option_id = spec.get('option_id')
            )

        return sku

    def update(self, instance, validated_data):

        specs = validated_data.pop('specs')


        with transaction.atomic():
            super().update(instance, validated_data)

            sku_specs = instance.specs.all()
            sku_specs_li = [{
                                'spec_id': spec.spec_id,
                                'option_id': spec.option_id
                             }
                            for spec in sku_specs]
            if specs != sku_specs_li:
                sku_specs.delete()
            for spec in specs:
                SKUSpecification.objects.create(
                    sku=instance,
                    spec_id=spec.get('spec_id'),
                    option_id=spec.get('option_id')
                )

        return instance