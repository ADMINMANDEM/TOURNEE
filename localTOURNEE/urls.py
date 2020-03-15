from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from tournee import views as tournee_views

# These urls are the 2 main strands - "admin" is for managing the website and "tournee" contains the part of the
# website I created
# they would look like: http://127.0.0.1:8000/tournee/
urlpatterns = [
    path('admin/', admin.site.urls),
    path('tournee/', include('tournee.urls')),
    path('', RedirectView.as_view(url='tournee/'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# These urls are used for accounts on the website (creation and logging in etc.)
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^signup/$', tournee_views.signup, name='signup'),
    url(r'^profile/$', tournee_views.update_player, name='profile')
]
