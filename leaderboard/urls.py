from django.urls import path

from . import views

urlpatterns = [
    # ex: /api/driver/5/team
    path("api/driver/", views.get_drivers, name="get_drivers"),
    path("api/driver/<int:driver_id>", views.get_driver, name="get_driver"),
    path("", views.leaderboard_page, name="leaderboards"),
]
