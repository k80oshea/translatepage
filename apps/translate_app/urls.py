from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.home),
    url(r'^lang/(?P<lang>\d+)$', views.change_lang),
    url(r'^login$', views.login_page),
    url(r'^user/login$', views.login),
    url(r'^user/signup$', views.signup),
    url(r'^newuser$', views.add_user),
    url(r'^user/add$', views.admin_add),
    url(r'^edit/langs$', views.make_changes),
    url(r'^newtext$', views.add_lang),    
    url(r'^edit/(?P<text_id>\d+)$', views.edit),
    url(r'^change/(?P<text_id>\d+)$', views.change),   
    url(r'^delete/(?P<text_id>\d+)$', views.delete), 
    url(r'^logout$', views.logout)
]