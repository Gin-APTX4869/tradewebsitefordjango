from django.conf.urls import url
from .import views as trade

urlpatterns = [
	url(r'^$', trade.index, name="home"),
	url(r'^square/$', trade.seek, name="square"),
	url(r'^help/$', trade.help, name="help"),
	url(r'^contact/$', trade.contact, name="contact"),
	# 用户
	url(r'^(?P<id>\d+)/(?:(?P<slug>[\w-]+)/)?$', trade.profile, name='profile'),
	url(r'^setting/(?P<id>\d+)/$', trade.setting, name='setting'),
	url(r'^mygoods/$', trade.mygoods, name='mygoods'),
	# 物品
	url(r'^post/$', trade.post, name='post'),
	url(r'^seek/$', trade.seek_post, name='seek'),
	url(r'^detail/(?P<id>\d+)/edit/$', trade.update, name='update'),
	url(r'^detail/(?P<id>\d+)/delete/$', trade.delete, name='delete'),
	url(r'^list/$', trade.list, name='list'),
	url(r'^list/(?P<category_id>[0-9]+)/$', trade.list, name='list'),
	url(r'^detail/(?P<id>\d+)/$', trade.detail, name='detail'),
]
