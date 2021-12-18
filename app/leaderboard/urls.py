from django.urls import path

from . import views

urlpatterns = [
    ## api urls
    # ex: /api/driver/5/team
    path("api/driver/", views.get_drivers, name="get_drivers"),
    path("api/driver/<int:driver_id>", views.get_driver, name="get_driver"),
    ## html urls
    path(
        "drivers_standings/<int:championship_id>",
        views.drivers_standings,
        name="drivers_standings",
    ),
    path(
        "constructors_standings/<int:championship_id>",
        views.constructors_standings,
        name="constructors_standings",
    ),
    path(
        "",
        views.latest_drivers_standings,
        name="index",
    ),
]
