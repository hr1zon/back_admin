from rest_framework import serializers

from goods.models import SPUSpecification, SPU, SpecificationOption


class SpecSerializer(serializers.ModelSerializer):
    '''spu规格获取序列化器类'''
    spu = serializers.StringRelatedField(label='spu名称')
    spu_id = serializers.IntegerField(label='spu id')
    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id')


class SpecsOptionSerializer(serializers.ModelSerializer):
    '''规格选项信息序列化器类'''

    spec = serializers.StringRelatedField(label='规格名称')
    spec_id = serializers.IntegerField(label='规格ID')
    class Meta:
        model = SpecificationOption
        exclude = ('create_time', 'update_time')


