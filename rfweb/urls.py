import os.path

from django.conf import settings
from django.conf.urls import include, patterns, url

from rfweb.rfwebapp import views

from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover, dajaxice_config
dajaxice_autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
    (r'^upload/?$', views.upload),
    (r'^search/?$', views.search),
    (r'^suite/(.*)', views.suite),
    (r'^suite_csv/(.*)', views.suite_csv),
    (r'^suite_md/(.*)', views.suite_md),
    (r'^results_csv/', views.results_csv),
    (r'^results_md/', views.results_md),
    (r'^create_task/?$', views.create_task),
    (r'^tasks/?$', views.tasks),
    (r'^results/$', views.results),
    (r'^download/([\w\d_-]+_[.\w\d-]+_[\d]+).zip', views.results_zip),
    (r'results/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.RESULTS_PATH, 'show_indexes':True}),
    (r'^log/?$', views.log),
    (r'^$', views.index),
)

urlpatterns += staticfiles_urlpatterns()
