from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('tournee/', include('tournee.urls')),
    path('admin/', admin.site.urls),
]


urlpatterns += [
    path('', RedirectView.as_view(url='tournee/', permanent=True)),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)