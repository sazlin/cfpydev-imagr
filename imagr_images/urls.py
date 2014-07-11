from django.conf.urls import patterns, url

from imagr_images import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^home/',views.home_page, name='home_page'),
    url(r'^login/$', views.user_login, name='user_login'),
)
