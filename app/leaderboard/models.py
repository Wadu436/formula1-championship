import datetime
import json
import math
from collections import defaultdict
from itertools import chain
from typing import Optional

from colorfield.fields import ColorField
from django.core import serializers, validators
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q
from django.db.models.query import QuerySet
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField


# Create your models here.
class Track(models.Model):
    location = models.CharField(max_length=64)  # Country or City
    name = models.CharField(max_length=64, null=True, blank=True)
    abbreviation = models.CharField(max_length=8)
    country = CountryField()

    full_laps = models.IntegerField(verbose_name="Laps in a full race (100%)")
    long_laps = models.IntegerField(verbose_name="Laps in a long race (50%)")
    medium_laps = models.IntegerField(verbose_name="Laps in a mediun race (25%)")

    overview_image = models.ImageField(null=True, blank=True, default=None)
    detail_image = models.ImageField(null=True, blank=True, default=None)

    def __str__(self):
        return f"{self.location}"

    def fastest_laps(self) -> QuerySet["RaceEntry"]:
        return RaceEntry.objects.filter(race__track=self).order_by("best_lap_time")


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
    class RaceLength(models.TextChoices):
        FULL = "F", _("Full Race (100%)")
        LONG = "L", _("Long Race (50%)")
        MEDIUM = "M", _("Medium Race (25%)")
        SHORT = "S", _("Short Race (5 laps)")

    championship_order = models.IntegerField(validators=[MinValueValidator(1)])
    championship = models.ForeignKey(
        Championship, on_delete=models.CASCADE, related_name="races"
    )
    track = models.ForeignKey(Track, on_delete=models.RESTRICT, related_name="races")

    date_time = models.DateTimeField(blank=True, null=True)
    finished = models.BooleanField(default=False)

    wet_race = models.BooleanField(default=False)

    length = models.CharField(
        max_length=1,
        choices=RaceLength.choices,
    )

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
        dna_entries: QuerySet[RaceEntry] = self.dna_entries.all()
        player_entries: QuerySet[RaceEntry] = self.race_entries.filter(bot=False)
        bot_entries: QuerySet[RaceEntry] = self.race_entries.filter(bot=True)
        entries = self.race_entries.all()

        fastest_entry: RaceEntry = self.race_entries.order_by("best_lap_time").first()

        num_entries = len(dna_entries) + len(player_entries)

        if num_entries == 0 or self.finished == False:
            return (dict(), dict())

        # Calculate Points
        total_points = {
            entry: SCORING_SYSTEM.get(entry.finish_position, 0) for entry in entries
        }

        # Fastest driver points
        if fastest_entry.finish_position >= 10:
            total_points[fastest_entry] += 1

        player_points: dict[Driver, int | float] = {
            entry.driver: total_points[entry] for entry in player_entries
        }
        bot_points: list[int | float] = [total_points[entry] for entry in bot_entries]

        # Distribute DNA points
        if len(dna_entries) > 0:
            # Sum of the first #DNA_ENTRIES bot scores
            total_bot_points = sum(sorted(bot_points, reverse=True)[: len(dna_entries)])
            print(sorted(bot_points, reverse=True))
            print(total_bot_points)
            dna_score = total_bot_points / (
                2 * len(dna_entries)
            )  # DNA Drivers receive half points
            print(dna_score)
            dna_score = round(dna_score, 1)
            print(dna_score)
            if dna_score > 0:
                for entry in dna_entries:
                    player_points[entry.driver] = dna_score
            else:
                for entry in dna_entries:
                    player_points[entry.driver] = 0
            

        # Calculate Team Scores
        team_points: dict[Team, int | float] = {
            entry.team: 0 for entry in chain(player_entries, dna_entries)
        }

        for entry in chain(player_entries, dna_entries):
            team_points[entry.team] += player_points[entry.driver]

        return (player_points, team_points)

    def winner(self) -> Optional["RaceEntry"]:
        if self.finished:
            winning_entry = self.race_entries.get(finish_position=1)
            return winning_entry

        return None

    def laps(self) -> int:
        track: Track = self.track
        match self.length:
            case "S":
                return 5
            case "M":
                return track.medium_laps
            case "L":
                return track.long_laps
            case "F":
                return track.full_laps

    def podium(self) -> list[Optional["RaceEntry"]]:
        podium = []
        for entry in self.race_entries.order_by("finish_position"):
            while len(podium) < entry.finish_position - 1 and len(podium) < 3:
                podium.append(None)
            if len(podium) >= 3:
                return podium
            podium.append(entry)
        while len(podium) < 3:
            podium.append(None)
        return podium

    def match_history(self) -> list[tuple["RaceEntry", int]]:
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
        dna_entries: QuerySet[RaceEntry] = self.dna_entries.all()
        player_entries: QuerySet[RaceEntry] = self.race_entries.filter(bot=False)
        bot_entries: QuerySet[RaceEntry] = self.race_entries.filter(bot=True)
        entries: QuerySet[RaceEntry] = self.race_entries.order_by('finish_position')

        fastest_entry: RaceEntry = self.race_entries.order_by("best_lap_time").first()

        num_entries = len(dna_entries) + len(player_entries)

        if num_entries == 0 or self.finished == False:
            return (dict(), dict())

        # Calculate Points
        total_points = {
            entry: SCORING_SYSTEM.get(entry.finish_position, 0) for entry in entries
        }

        # Fastest driver points
        if fastest_entry.finish_position >= 10:
            total_points[fastest_entry] += 1

        return [(entry, total_points[entry]) for entry in entries]
        


class RaceEntry(models.Model):
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name="race_entries",
    )
    driver = models.ForeignKey(
        Driver,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="race_entries",
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="race_entries",
    )

    bot = models.BooleanField(verbose_name="Is Bot", default=False)

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

    tires = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["race", "driver"], name="raceentry_unique_driver_race"
            ),
            models.CheckConstraint(
                check=(
                    Q(
                        bot=True,
                        driver__isnull=True,
                        team__isnull=True,
                        best_lap_time__isnull=False,
                        finish_position__isnull=False,
                    )
                    | Q(
                        bot=False,
                        driver__isnull=False,
                        team__isnull=False,
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
        if not self.bot:
            return f"P{self.finish_position}: {self.driver}"
        else:
            return f"P{self.finish_position}: Bot"


class DNAEntry(models.Model):
    race = models.ForeignKey(Race, on_delete=models.CASCADE, related_name="dna_entries")
    driver = models.ForeignKey(
        Driver, on_delete=models.RESTRICT, related_name="dna_entries"
    )
    team = models.ForeignKey(
        Team, on_delete=models.RESTRICT, related_name="dna_entries"
    )
