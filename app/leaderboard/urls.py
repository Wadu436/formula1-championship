from django.urls import path

from . import views

urlpatterns = [
    # ex: /api/driver/5/team
    path("api/driver/", views.get_drivers, name="get_drivers"),
    path("api/driver/<int:driver_id>", views.get_driver, name="get_driver"),
    path(
        "drivers_standings/<int:championship_id>",
        views.drivers_standings,
        name="drivers_standings",
    ),
    path(
        "drivers_standings/latest/",
        views.latest_drivers_standings,
        name="latest_drivers_standings",
    ),
    path("championships/", views.championships, name="championships"),
    path(
        "",
        views.index,
        name="index",
    ),
]
