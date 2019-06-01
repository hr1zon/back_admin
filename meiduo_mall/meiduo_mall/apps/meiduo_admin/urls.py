from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from meiduo_admin.views import users, statistical, channels, skus, spus, orders

urlpatterns = [

    url(r'^authorizations/$', users.AdminAuthorizeView.as_view()),

    # 数据统计
    url(r'^statistical/total_count/$', statistical.UserTotalCountView.as_view()),
    url(r'^statistical/day_increment/$', statistical.UserDayCountView.as_view()),
    url(r'^statistical/day_active/$', statistical.UserActiveAcountView.as_view()),
    url(r'^statistical/day_orders/$', statistical.UserOrderCountView.as_view()),
    url(r'^statistical/month_increment/$', statistical.UserMonthCountView.as_view()),
    url(r'^statistical/goods_day_views/$', statistical.GoodsDayView.as_view()),

    # 用户信息
    url(r'^users/$', users.UserInfoView.as_view()),

    # 获取频道组数据
    url(r'^goods/channel_types/$', channels.ChannelTypesView.as_view()),
    # 获取一级分类数据
    url(r'^goods/categories/$', channels.ChannelCategoryView.as_view()),

    # 获取sku商品数据
    url(r'^skus/simple/$', skus.SKUSimpleView .as_view()),

    # 获取第三级分类数据
    url(r'^skus/categories/$', skus.SKUCategoriesView.as_view()),

    # 获取SPU数据
    url(r'^goods/simple/', spus.SPUSimpleView.as_view()),

    # 获取SPU规格信息
    url(r'^goods/(?P<pk>\d+)/specs/', spus.SPUSpecView.as_view()),


]
# 商品管理
router = DefaultRouter()
router.register('goods/channels', channels.ChannelViewSet, base_name='channels')
urlpatterns += router.urls

# 图片管理
router = DefaultRouter()
router.register('skus/images', skus.SKUImageViewSet, base_name='iamges')
urlpatterns += router.urls

# sku管理
router = DefaultRouter()
router.register('skus', skus.SKUViewSet, base_name='skus')
urlpatterns += router.urls

# 订单管理
router = DefaultRouter()
router.register('orders', orders.OrdersViewSet, base_name='orders')
urlpatterns += router.urls
print(router.urls)