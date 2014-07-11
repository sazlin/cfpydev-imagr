from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from imagr_images import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^home/',views.home_page, name='home_page'),
    url(r'^login/$', views.user_login, name='user_login'),
    # url(r'^media/' settings.MEDIA_ROOT)
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
