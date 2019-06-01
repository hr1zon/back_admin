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
