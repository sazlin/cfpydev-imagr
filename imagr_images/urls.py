from django.conf.urls import patterns, url

from imagr_images import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index')
)
