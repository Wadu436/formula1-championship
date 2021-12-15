from django.contrib import admin

from . import models


# Register your models here.
@admin.register(models.Team, site=admin.site)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Track, site=admin.site)
class TrackAdmin(admin.ModelAdmin):
    list_display = ("location", "name")


@admin.register(models.Championship, site=admin.site)
class ChampionshpipAdmin(admin.ModelAdmin):
    list_display = ("name",)


@admin.register(models.Driver, site=admin.site)
class DriverAdmin(admin.ModelAdmin):
    list_display = ("name", "team")


class RaceEntryInline(admin.TabularInline):
    model = models.RaceEntry
    template = "leaderboard/admin/raceentry_tabular_inline.html"

    class Media:
        js = (
            "leaderboard/jquery-3.6.0.min.js",
            "leaderboard/admin/raceentry_tabular.js",
        )


@admin.register(models.Race, site=admin.site)
class RaceAdmin(admin.ModelAdmin):
    list_display = ("__str__", "championship", "track")
    list_filter = ("championship", "track")
    inlines = [
        RaceEntryInline,
    ]
    # change_form_template = "leaderboard/admin/race_change_form.html"
