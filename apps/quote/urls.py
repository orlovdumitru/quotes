
from django.conf.urls import url
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.tohome),
    path('main', views.index),
    path('login', views.login),
    path('new_user', views.new_user),
    path('logout', views.logout),
    path('quotes', views.quotes),
    path('newquote', views.newquote),
    re_path('quotedby/(?P<id>\d+)/$', views.quoted_by),
    re_path('addfav/(?P<id>\d+)/$', views.add_fav),
    re_path('display/(?P<id>\d+)/$', views.display),
    # url(r'^(?P<id>\d+)$', views.display),
]
