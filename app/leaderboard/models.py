import datetime
import json
import math
from collections import defaultdict

from colorfield.fields import ColorField
from django.core import serializers, validators
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django_countries.fields import CountryField


# Create your models here.
class Track(models.Model):
    location = models.CharField(max_length=64)  # Country or City
    name = models.CharField(max_length=64, null=True, blank=True)
    abbreviation = models.CharField(max_length=8)
    country = CountryField()

    def __str__(self):
        return f"{self.location}"


class Team(models.Model):
    name = models.CharField(max_length=64)
    full_name = models.CharField(max_length=64)
    color = ColorField(default="#FF0000")
    country = CountryField()

    def __str__(self):
        return f"{self.name}"


class Championship(models.Model):
    name = models.CharField(max_length=64)
    start_date = models.DateField()

    def __str__(self):
        return f"{self.name}"

    def get_drivers_standings(
        self, first_race=None, last_race=None
    ) -> list[tuple["Driver", int | float]]:
        first_race = first_race or 0
        last_race = last_race or self.races.count()

        race_scores: list[dict["Driver", int | float]] = [
            race.get_points()[0] for race in self.races.all()
        ]

        total_points: dict["Driver", int | float] = defaultdict(int)
        for race in race_scores:
            for driver, points in race.items():
                total_points[driver] += points

        total_points_list = [
            (driver, points) for driver, points in total_points.items()
        ]

        total_points_list.sort(key=lambda item: (-item[1], item[0].name))

        return total_points_list

    def get_constructors_standings(
        self, first_race=None, last_race=None
    ) -> list[tuple["Team", int | float]]:
        first_race = first_race or 0
        last_race = last_race or self.races.count()

        team_scores: list[dict["Team", int | float]] = [
            race.get_points()[1] for race in self.races.all()
        ]

        total_points: dict["Team", int | float] = defaultdict(int)
        for race in team_scores:
            for team, points in race.items():
                total_points[team] += points

        total_points_list = [(team, points) for team, points in total_points.items()]

        total_points_list.sort(key=lambda item: (-item[1], item[0].name))

        return total_points_list

    class Meta:
        get_latest_by = "start_date"


class Driver(models.Model):
    name = models.CharField(max_length=64)
    nickname = models.CharField(max_length=64, null=True, blank=True)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.RESTRICT)
    country = CountryField()

    def __str__(self):
        return f"{self.name}"

    def get_dict(self):
        data = {
            "id": self.pk,
            "name": self.name,
            "team": self.team.pk if self.team else None,
        }
        return data


class Race(models.Model):
    championship_order = models.IntegerField(validators=[MinValueValidator(1)])
    championship = models.ForeignKey(
        Championship, on_delete=models.CASCADE, related_name="races"
    )
    track = models.ForeignKey(Track, on_delete=models.RESTRICT)

    date_time = models.DateTimeField(blank=True, null=True)
    finished = models.BooleanField(default=False)

    wet_race = models.BooleanField(default=False)

    schedule_image = models.ImageField(blank=True, null=True)
    detail_image = models.ImageField(blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["championship_order", "championship"],
                name="race_unique_championship_order",
            )
        ]

    def __str__(self):
        return (
            f"{self.championship} Race {self.championship_order}: {self.track.location}"
        )

    def get_points(self) -> tuple[dict[Driver, int | float], dict[Team, int | float]]:
        # TODO: Properly handle fastest lap if fastest lap goes to bot or driver below 10th place
        SCORING_SYSTEM = {
            1: 25,
            2: 18,
            3: 15,
            4: 12,
            5: 10,
            6: 8,
            7: 6,
            8: 4,
            9: 2,
            10: 1,
        }

        # Get entries
        dna_entries: QuerySet[RaceEntry] = self.race_entries.filter(dna=True)
        non_dna_entries: QuerySet[RaceEntry] = self.race_entries.filter(dna=False)
        entries: QuerySet[RaceEntry] = self.race_entries.all()

        if len(entries) == 0:
            return (dict(), dict())

        points = dict()

        # Setup data for fastest lap
        fastest_driver = None
        fastest_time = None

        # Setup data for DNA points
        bot_positions = [i + 1 for i in range(len(dna_entries) + len(non_dna_entries))]

        for entry in non_dna_entries:
            # Check fastest lap
            if not fastest_time or entry.best_lap_time < fastest_time:
                fastest_driver = entry.driver
                fastest_time = entry.best_lap_time

            # Figure out which positions were taken by bots
            if entry.finish_position in bot_positions:
                bot_positions.remove(entry.finish_position)

            points[entry.driver] = SCORING_SYSTEM.get(entry.finish_position, 0)

        # If for some reason the number of left-over positions are
        # greater than the number of DNAs, only take the appropriate number
        bot_positions = bot_positions[: len(dna_entries)]

        # Assign fastest lap point
        points[fastest_driver] += 1

        # Calculate score each DNA driver gets
        if dna_entries:
            dna_score = sum(
                SCORING_SYSTEM[position] if position in SCORING_SYSTEM else 0
                for position in bot_positions
            )
            dna_score /= 2 * len(dna_entries)  # DNA drivers receive half points

            for entry in dna_entries:
                points[entry.driver] = dna_score

        # Find all Driver's Team
        teams: dict[Team, int | float] = {entry.team: 0 for entry in entries}

        for entry in entries:
            teams[entry.team] += points[entry.driver]

        return (points, teams)


class RaceEntry(models.Model):
    race = models.ForeignKey(
        Race, on_delete=models.CASCADE, related_name="race_entries"
    )
    driver = models.ForeignKey(Driver, on_delete=models.RESTRICT)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT)

    dna = models.BooleanField(verbose_name="Did Not Attend", default=False)

    # Should be not null if not DNA
    qualifying_position = models.IntegerField(
        verbose_name="Qualifying Position",
        validators=[MinValueValidator(1)],
        null=True,
        blank=True,
    )
    grid_penalty = models.PositiveIntegerField(default=0)
    finish_position = models.IntegerField(
        validators=[MinValueValidator(1)], null=True, blank=True
    )

    best_lap_time = models.DurationField(null=True, blank=True)

    pit_stops = models.PositiveIntegerField(default=1, null=True, blank=True)

    dnf = models.BooleanField(
        verbose_name="Did Not Finish", default=False, null=True, blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["race", "driver"], name="raceentry_unique_driver_race"
            ),
            models.CheckConstraint(
                check=(
                    Q(dna=True)
                    | Q(
                        qualifying_position__isnull=False,
                        grid_penalty__isnull=False,
                        finish_position__isnull=False,
                        best_lap_time__isnull=False,
                        pit_stops__isnull=False,
                        dnf__isnull=False,
                    )
                ),
                name="raceentry_dna_notnull",
            ),
        ]

    def __str__(self):
        return (
            f"P{self.finish_position}: {self.driver}"
            if not self.dna
            else f"DNA: {self.driver}"
        )
