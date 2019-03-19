

from django.conf.urls import url
from . import views

app_name = 'upload'
urlpatterns = [
    url(r'^$', views.upload, name='upload'),
    url(r'^upload/$',views.upload,name='upload'),
    url(r'^model_form_upload',views.model_form_upload,name='model_form_upload'),
    url(r'^upload_video',views.upload_video,name='upload_video'),
    url(r'^show_uploaded',views.show_uploaded,name = 'show_uploaded')
]
