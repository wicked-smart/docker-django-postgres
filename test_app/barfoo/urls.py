from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name="index"),
    path("flight/<int:flight_id>", views.flight, name="flight"),
    path("<int:flight_id>/book", views.book_flight, name="book")
]

urlpatterns += static(settings.STATIC_URL, document=settings.STATIC_ROOT)