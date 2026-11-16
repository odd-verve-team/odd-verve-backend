from django.urls import path

from apps.notifications.views import (
    NotificationListView,
    NotificationBuyArtworkView,
    NotificationBecomeArtistView,
)

urlpatterns = [
    path("", NotificationListView.as_view(), name="notifications_list"),
    path(
        "buy-artwork/",
        NotificationBuyArtworkView.as_view(),
        name="buy_artwork_notification",
    ),
    path(
        "become-artist/",
        NotificationBecomeArtistView.as_view(),
        name="become_artist_notification",
    ),
]
