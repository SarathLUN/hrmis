from django.conf.urls import include, url
from django.contrib import admin
from HRM import views

urlpatterns = [
    # Examples:
    # url(r'^$', 'HRM.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^hr/', include('hr.urls', namespace="hr")),
    url(r'^holiday/', include('holiday.urls', namespace="holiday")),
    url(r'^leave/', include('leave.urls', namespace='leave')),
    url(r'^attendance/', include('attendance.urls', namespace='attendance')),
    url(r'^account/', include('account.urls', namespace='account')),
    url(r'^admin_action/', include('admin_action.urls', namespace='admin_action')),
    url(r'^$', views.login, name="start"),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^home/$', views.home, name='home'),
    url(r'^features/$', views.features, name='features'),
]
