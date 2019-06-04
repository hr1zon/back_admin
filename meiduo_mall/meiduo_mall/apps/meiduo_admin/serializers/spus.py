from rest_framework import serializers

from goods.models import SPU, SPUSpecification, SpecificationOption


class SPUSimpleSerializer(serializers.ModelSerializer):
    '''SPU数据序列化器类'''
    class Meta:
        model = SPU
        fields = ('id', 'name')


class SpecOptionSerializer(serializers.ModelSerializer):
    '''规格选项序列化器类'''
    class Meta:
        model = SpecificationOption
        fields = ('id', 'value')

class SPUSpecSerializer(serializers.ModelSerializer):
    '''SPU规格信息序列化器类'''

    spu = serializers.StringRelatedField(label='spu商品名称')
    options = SpecOptionSerializer(label='规格选项', many=True)
    spu_id = serializers.IntegerField(label='spu商品ID')
    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id', 'options')



class SPUSerializer(serializers.ModelSerializer):
    '''获取SPU商品数据详情'''

    brand = serializers.StringRelatedField(label='品牌名称')
    brand_id = serializers.IntegerField(label='品牌ID')
    category1 = serializers.StringRelatedField(label='一级分类名称')
    category2 = serializers.StringRelatedField(label='二级分类名称')
    category3 = serializers.StringRelatedField(label='三级分类名称')
    category1_id = serializers.IntegerField(label='一级分类ID')
    category2_id = serializers.IntegerField(label='一级分类ID')
    category3_id = serializers.IntegerField(label='一级分类ID')
    class Meta:
        model = SPU
        exclude = ('create_time', 'update_time')

    def create(self, validated_data):
        print(validated_data)
        spu = SPU.objects.create(**validated_data)
        return spu