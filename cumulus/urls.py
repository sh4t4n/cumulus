from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'cumulus.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^/?$', 'vfm.views.commander'),
    url(r'^upload/$', 'vfm.views.uploadFile'),
    url(r'^mkdir/$', 'vfm.views.createDirectory'),
    url(r'^rename/$', 'vfm.views.rename'),
    #auth
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout'),
]
