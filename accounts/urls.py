from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.homepage),
    url(r'^login/$', views.user_login),
    url(r'^register/confirm/(?P<id>\d+)/$', views.confirm_account),
    url(r'^register/$', views.custom_user_register),
    url(r'^logout/$', views.user_logout),
    url(r'^password/reset/confirm/(?P<id>\d+)/$', views.reset_password),
    url(r'^password/reset/', views.reset_password_email),
    url(r'^password/update/(?P<pk>\d+)/$', views.update_password),
    url(r'^user/get/(?P<pk>\d+)/$', views.UserDetail.as_view()),
    url(r'^user/deactivate/$', views.deactivate_account),
    url(r'^user/make/profile/', views.UserProfileList.as_view()),
    url(r'^user/get/profile/(?P<pk>\d+)/', views.UserProfileDetail.as_view()),
    url(r'^institute/make/profile/', views.InstituteProfileList.as_view()),
    url(r'^institute/get/profile/(?P<pk>\d+)/', views.InstituteProfileDetail.as_view()),
    url(r'^user/follow/', views.follow),
    url(r'^user/get/following', views.get_my_following),
    url(r'^user/get/followers', views.get_my_followers),
    url(r'^user/get/notifications', views.get_notifications),
    url(r'^user/get/categories', views.get_categories),
    url(r'^user/update/notification/(?P<pk>\d+)/', views.update_notificaiton),
]
