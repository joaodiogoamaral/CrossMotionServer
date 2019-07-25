

from django.conf.urls import url,include
from django.contrib.auth import views as auth_views
from . import views
from django.views.generic.base import TemplateView

app_name = 'upload'
urlpatterns = [
    #url(r'^$', views.upload, name='upload'),
    url(r'^upload/$',views.upload,name='upload'),
    url(r'^model_form_upload',views.model_form_upload,name='model_form_upload'),
    url(r'^login',auth_views.login,name='login'),
    url(r'^upload_video',views.upload_video,name='upload_video'),
    url(r'^uploadlogin',views.uploadlogin,name = 'uploadlogin'),
    url(r'^show_uploaded/',views.show_uploaded,name = 'show_uploaded'),
    url(r'^feedback/(?P<video_name>[\w.]+)$',views.feedback,name='feedback'),
    url(r'^signup/',views.SignUp.as_view(),name = 'signup'),
] 
