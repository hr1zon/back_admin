import re

from django.utils import timezone
from rest_framework import serializers
from rest_framework_jwt.settings import api_settings

from users.models import User


class AdminAuthSerialier(serializers.ModelSerializer):
    '''
        1.确认所需字段
        2.确认字段read/write_only
        3.校验时是否需要补充验证
        4.是否需要重写create方法
    '''
    token = serializers.CharField(label='JWT token', read_only=True)
    username = serializers.CharField(label='用户名')
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'token')
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def validate(self, attrs):
        '''补充验证用户名和密码是否存在'''
        username = attrs['username']
        password = attrs['password']

        try:
            user = User.objects.get(username=username, is_staff=True)
        except User.DoesNotExist:
            raise serializers.ValidationError('用户名或密码错误')
        else:
            if not user.check_password(password):
                raise serializers.ValidationError('用户名或密码错误')

        attrs['user'] = user

        return attrs

    def create(self, validated_data):
        '''生成jwt token 并保存用户信息'''
        user = validated_data['user']

        # 更新登录时间
        date = timezone.now()
        user.last_login = date
        user.save()

        # 生成jwt token
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        # 给user增加token属性
        user.token = token

        return user


class UserSerializer(serializers.ModelSerializer):
    '''用户序列化器'''
    class Meta:
        model = User
        fields = ('id', 'username', 'mobile', 'email', 'password')

        extra_kwargs = {
            'username': {
                'min_length': 5,
                'max_length': 20,
                'error_messages': {
                    'min_length': '用户名最小长度为5',
                    'max_length': '用户名最大长度为20'
                }
            },
            'password': {
                'write_only': True,
                'min_length': 8,
                'max_length': 20,
                'error_messages': {
                    'min_length': '密码最小长度为8',
                    'max_length': '密码最大长度为20'
                }
            }
        }

    def validate_mobile(self, value):

        if not re.match(r'1[3-9]\d{9}$', value):
            raise serializers.ValidationError('手机号格式错误')

        res = User.objects.filter(mobile=value).count()

        if res > 0:
            raise serializers.ValidationError('手机号已注册')
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
