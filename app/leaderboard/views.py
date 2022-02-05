import json
from typing import Optional

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import FAQ, Championship, Driver, Race, RuleChapter, Track
from .stats import stats_pace


# API views
def get_drivers(request):
    return HttpResponse(
        json.dumps([driver.get_dict() for driver in Driver.objects.all()]),
        content_type="application/json",
    )


def get_driver(request, driver_id):
    driver = Driver.objects.get(pk=driver_id)
    return HttpResponse(json.dumps(driver.get_dict()), content_type="application/json")


# HTML views
def drivers_standings(request, championship_id):
    championship = Championship.objects.filter(id=championship_id).first()
    if championship:
        context = {
            "current_championship": championship,
            "championships": Championship.objects.all(),
            "in_championship": True,
        }
        return render(request, "leaderboard/drivers_standings.html", context=context)
    else:
        return latest_drivers_standings(request)


def constructors_standings(request, championship_id):
    championship = Championship.objects.filter(id=championship_id).first()
    if championship:
        context = {
            "current_championship": Championship.objects.get(id=championship_id),
            "championships": Championship.objects.all(),
            "in_championship": True,
        }
        return render(
            request, "leaderboard/constructors_standings.html", context=context
        )
    else:
        return latest_constructors_standings(request)


def races(request, championship_id):
    championship = Championship.objects.filter(id=championship_id).first()
    if championship:
        context = {
            "current_championship": championship,
            "championships": Championship.objects.all(),
            "in_championship": True,
            "races": championship.races.order_by('championship_order')
        }
        return render(request, "leaderboard/races.html", context=context)
    else:
        return latest_races(request)


def track_overview(request):
    context = {
        "tracks": Track.objects.order_by("location"),
        "championships": Championship.objects.all(),
    }
    return render(request, "leaderboard/tracks.html", context=context)


def track_detail(request, track_id):
    track = Track.objects.filter(id=track_id).first()
    if track:
        last_race = track.races.filter(finished=True).order_by("date_time").last()
        context = {
            "track": track,
            "last_race": last_race,
            "championships": Championship.objects.all(),
        }
        return render(request, "leaderboard/track_detail.html", context=context)
    else:
        return redirect(reverse("track_overview"))


def match_history(request, race_id):
    race: Optional[Race] = Race.objects.filter(id=race_id).first()
    if race is not None:
        previous_race = Race.objects.filter(championship=race.championship, championship_order=race.championship_order-1).first()
        next_race = Race.objects.filter(championship=race.championship, championship_order=race.championship_order+1).first()
        context = {
            "race": race,
            "current_championship": race.championship,
            "championships": Championship.objects.all(),
            "in_championship": True,
            "fastest_lap": race.race_entries.order_by("best_lap_time").first(),
            "previous_race": previous_race,
            "next_race": next_race,
        }
        return render(request, "leaderboard/match_history.html", context=context)
    else:
        return latest_races(request)

def rules(request):
    context = {
        "championships": Championship.objects.all(),
        "rules": RuleChapter.objects.order_by('number'),
    }
    return render(request, "leaderboard/rules.html", context=context)

def faq(request):
    context = {
        "championships": Championship.objects.all(),
        "faq": FAQ.objects.all(),
    }
    return render(request, "leaderboard/faq.html", context=context)

def pace(request, championship_id):
    championship = Championship.objects.filter(id=championship_id).first()
    if championship:
        context = {
            "current_championship": championship,
            "championships": Championship.objects.all(),
            "in_championship": True,
            "pace_table": stats_pace(championship),
        }
        return render(request, "leaderboard/stats_pace.html", context=context)
    else:
        return latest_drivers_standings(request)

# Latest redirect views
def latest_drivers_standings(request):
    latest_championship = Championship.objects.latest("start_date")
    return redirect(reverse("drivers_standings", args=[latest_championship.id]))


def latest_constructors_standings(request):
    latest_championship = Championship.objects.latest("start_date")
    return redirect(reverse("constructors_standings", args=[latest_championship.id]))


def latest_races(request):
    latest_championship = Championship.objects.latest("start_date")
    return redirect(reverse("races", args=[latest_championship.id]))
