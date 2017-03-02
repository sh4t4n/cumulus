from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', 'vfm.views.commander'),
    url(r'^trash/?$', 'vfm.views.trashFolderView'),
    url(r'^upload/$', 'vfm.views.uploadFile'),
    url(r'^download/$', 'vfm.views.getDownload'),
    url(r'^mkdir/$', 'vfm.views.createDirectory'),
    url(r'^rename/$', 'vfm.views.rename'),
    url(r'^remove/$', 'vfm.views.moveToTrash'),
    url(r'^recovery/$', 'vfm.views.recovery'),
    url(r'^delete/$', 'vfm.views.delete'),
    url(r'^clean-trash/$', 'vfm.views.cleanTrash'),
    url(r'^trash-counter/$', 'vfm.views.trashCounter'),
    #auth
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
]
