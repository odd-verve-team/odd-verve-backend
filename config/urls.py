from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Список ендпоінтів API v1
api_v1_patterns = [
    path('auth/', include('apps.authentication.urls')),
    path('users/', include('apps.users.urls')),
    path('artworks/', include('apps.artworks.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
]

urlpatterns = [
    # Адмін-панель Django
    path('admin/', admin.site.urls),

    # Префікс для всіх ендпоінтів API
    path('api/v1/', include(api_v1_patterns)),
]

# Обслуговування медіафайлів у режимі розробки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)