import json

from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Championship, Driver


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
    context = {
        "current_championship": Championship.objects.get(id=championship_id),
        "championships": Championship.objects.all(),
    }
    return render(request, "leaderboard/drivers_standings.html", context=context)


def constructors_standings(request, championship_id):
    context = {
        "current_championship": Championship.objects.get(id=championship_id),
        "championships": Championship.objects.all(),
    }
    return render(request, "leaderboard/constructors_standings.html", context=context)


def latest_drivers_standings(request):
    latest_championship = Championship.objects.latest()
    return redirect(reverse("drivers_standings", args=[latest_championship.id]))
