from rest_framework import status
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, ListCreateAPIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from meiduo_admin.serializers.users import AdminAuthSerialier, UserSerializer
from users.models import User


class AdminAuthorizeView(CreateAPIView):
    serializer_class = AdminAuthSerialier


# class AdminAuthorizeView(APIView):
#     def post(self, request):
#         '''
#         1.获取参数并校验
#         2.生成jwt_token
#         3.响应
#         '''
#         serializer = AdminAuthSerialier(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data,status=status.HTTP_201_CREATED)

class UserInfoView(ListCreateAPIView):
    '''查询用户'''
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer

    def get_queryset(self):
        '''
            1.获取keyword关键字
            2.查询普通用户数据
            3.将数据序列化并返回响应

        '''

        keyword = self.request.query_params.get('keyword')

        if keyword is None or keyword == '':
            users = User.objects.filter(is_staff=False)
        else:
            users = User.objects.filter(is_staff=False, username__contains=keyword)

        return users




