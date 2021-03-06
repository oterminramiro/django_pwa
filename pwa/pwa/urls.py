from django.contrib import admin
from django.urls import include, path

from django.views.generic import TemplateView
from django.conf.urls import url

urlpatterns = [
	path('admin/', admin.site.urls),
	url(r'^$', TemplateView.as_view(template_name='index.html')),

	path('api/', include('api.urls')),
]
