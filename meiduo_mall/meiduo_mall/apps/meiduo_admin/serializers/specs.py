from rest_framework import serializers

from goods.models import SPUSpecification, SPU


class SpecSerializer(serializers.ModelSerializer):
    '''spu规格获取序列化器类'''
    spu = serializers.StringRelatedField(label='spu名称')
    spu_id = serializers.IntegerField(label='spu id')
    class Meta:
        model = SPUSpecification
        fields = ('id', 'name', 'spu', 'spu_id')

    # def update(self, instance, validated_data):
    #     print(validated_data)
    #     name = validated_data['name']
    #     spu_id = validated_data['spu_id']
    #     spu = SPU.objects.get(id=spu_id)
    #     instance.name = name
    #     instance.spu = spu
    #     instance.spu_id = spu_id
    #     instance.save()
    #     print(instance)
    #     return instance
