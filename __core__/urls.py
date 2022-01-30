from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from frontpage.views import DoneSummaryView

urlpatterns = [
	# url(r'^$', Frontpage.as_view(template_name='index.html'), name="home"),
	url(r'^', DoneSummaryView.as_view(), name="done_summary"),

	# url(r'^login/', auth_views.login,{"template_name":'masuk.html'}, name='login' ),
	#P url(r'^logout/', auth_views.logout,{"template_name":'keluar.html'}, name='logout' ),

	url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
	urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
