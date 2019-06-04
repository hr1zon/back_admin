from datetime import timedelta

from django.utils import timezone
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from goods.models import GoodsVisitCount
from meiduo_admin.serializers.statistical import GoodsVisitSerializer
from users.models import User


class UserTotalCountView(APIView):
    '''
        用户总数
        1.获取用户总数
        2.返回响应
    '''
    permission_classes = [IsAdminUser]
    def get(self,request):

        count = User.objects.count()

        date_now = timezone.now()

        date = date_now.date()

        context = {
            'date': date,
            'count': count
        }
        return Response(context)


class UserDayCountView(APIView):
    '''日增用户数量'''
    permission_classes = [IsAdminUser]

    def get(self,request):
        '''
            1.获取日增用户数量
            2.返回响应
        '''
        date_now = timezone.now()

        date = date_now.date()

        count = User.objects.filter(date_joined__gte=date_now.replace(hour=0, minute=0, second=0, microsecond= 0)).count()

        context = {
            'date': date,
            'count': count
        }

        return Response(context)


class UserActiveAcountView(APIView):
    '''日活跃用户'''
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
            1.获取日活跃参数
            2.返回响应

        '''
        date_now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        date = date_now.date()

        count = User.objects.filter(last_login__gte=date_now).count()

        context = {
            'date': date,
            'count': count
        }

        return  Response(context)


class UserOrderCountView(APIView):
    '''日下单用户量'''
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
            1.获取日下单用户量
            2.返回响应

        '''
        date_now = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        date = date_now.date()

        count = User.objects.filter(orders__create_time__gte=date_now).count()

        context = {
            'date': date,
            'count': count
        }

        return Response(context)


class UserMonthCountView(APIView):
    '''30天日增用户量'''
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
            1.获取30天每天的用户增量
            2.返回响应

        '''
        date_now= timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        begin_date = date_now - timedelta(29)

        count_list = []

        for i in range(30):
            cur_date = begin_date + timedelta(i)
            next_date = cur_date + timedelta(1)

            count = User.objects.filter(date_joined__gte=cur_date, date_joined__lt=next_date).count()
            count_list.append({
                'date': cur_date,
                'count': count
            })

        return Response(count_list)


class GoodsDayView(APIView):
    '''日分类商品访问量'''
    permission_classes = [IsAdminUser]

    def get(self, request):
        '''
            1.获取日分类商品访问量
            2.返回响应

        '''
        date_now = timezone.now().date()
        count = GoodsVisitCount.objects.filter(date=date_now)

        serializer = GoodsVisitSerializer(count, many=True)

        return Response(serializer.data)