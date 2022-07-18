from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    ## api urls
    # ex: /api/driver/5/team
    path("api/driver/", views.get_drivers, name="get_drivers"),
    path("api/driver/<int:driver_id>", views.get_driver, name="get_driver"),
    ## html urls
    path(
        "championships/<int:championship_id>/drivers_standings/",
        views.drivers_standings,
        name="drivers_standings",
    ),
    path(
        "championships/<int:championship_id>/constructors_standings/",
        views.constructors_standings,
        name="constructors_standings",
    ),
    path(
        "championships/<int:championship_id>/races/",
        views.races,
        name="races",
    ),
    path(
        "tracks/",
        views.track_overview,
        name="track_overview",
    ),
    path(
        "tracks/<int:track_id>/",
        views.track_detail,
        name="track_detail",
    ),
    path(
        "rules/",
        views.rules,
        name="rules",
    ),
    path("match_history/<int:race_id>/", views.match_history, name="match_history"),
    path("sprint_match_history/<int:race_id>/", views.sprint_match_history, name="sprint_match_history"),
    path("faq/", views.faq, name="faq"),
    path("championships/<int:championship_id>/stats/", views.stats, name="stats"),
    path(
        "",
        views.index,
        name="index",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
