from django.conf.urls import url
from rest_framework.routers import DefaultRouter

from meiduo_admin.views import users, statistical, channels, skus, spus, orders, brands, categories, specs

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

    # 获取SPU简单数据
    url(r'^goods/simple/', spus.SPUSimpleView.as_view()),

    # 获取SPU规格信息
    url(r'^goods/(?P<pk>\d+)/specs/', spus.SPUSpecView.as_view()),

    # 获取品牌下拉列表
    url(r'^goods/brands/simple/', brands.BrandSimpleView.as_view()),

    # 获取类型下拉列别
    url(r'^goods/channel/categories/$', categories.GoodsCategorySimpleView.as_view({'get':'list'})),
    url(r'^goods/channel/categories/(?P<pk>\d+)/$', categories.GoodsCategorySimpleView.as_view({'get':'retrieve'})),

    # 添加SPU商品时插入图片
    url(r'^goods/images/', spus.SPUImagesView.as_view()),

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


# 品牌管理
router = DefaultRouter()
router.register('goods/brands', brands.BrandsViewSet, base_name='brands')
urlpatterns += router.urls


# SPU管理
router = DefaultRouter()
router.register('goods', spus.SPUViewSet, base_name='goods')
urlpatterns += router.urls

# 规格管理
router = DefaultRouter()
router.register('goods/specs', specs.SpecsViewSet, base_name='specs')
urlpatterns += router.urls
