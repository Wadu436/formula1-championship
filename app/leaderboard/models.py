import math
from collections import defaultdict
from decimal import Decimal
from itertools import chain
from typing import Optional

from colorfield.fields import ColorField
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
        return (
            RaceEntry.objects.filter(race__track=self)
            .exclude(best_lap_time=None)
            .order_by("best_lap_time")
        )

    class Meta:
        ordering = ("location",)


class Team(models.Model):
    name = models.CharField(max_length=64)
    full_name = models.CharField(max_length=64)
    color = ColorField(default="#FF0000")
    country = CountryField()

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ("name",)


class Driver(models.Model):
    name = models.CharField(max_length=64)
    nickname = models.CharField(max_length=64, null=True, blank=True)
    team = models.ForeignKey(Team, null=True, blank=True, on_delete=models.RESTRICT)
    country = CountryField()
    number = models.IntegerField(
        verbose_name="Driver Number", null=True, blank=True, unique=True
    )

    def __str__(self):
        return f"{self.name}"

    def get_dict(self):
        data = {
            "id": self.pk,
            "name": self.name,
            "team": self.team.pk if self.team else None,
        }
        return data

    class Meta:
        ordering = ("name",)


class Championship(models.Model):
    name = models.CharField(max_length=64)
    start_date = models.DateField()
    # drivers = models.ManyToManyField(Driver, blank=True)
    drivers = models.ManyToManyField(Driver, blank=True, through="ChampionshipDriver")

    races: QuerySet["Race"]

    def __str__(self):
        return f"{self.name}"

    def get_driver_team_map(self) -> dict[int, Team]:
        # Initialize with base teams
        driver_team_map = {
            driver.id: driver.team
            for driver in Driver.objects.all().select_related("team")
        }

        for cd in ChampionshipDriver.objects.filter(championship=self).select_related(
            "team"
        ):
            if cd.team:
                driver_team_map[cd.driver_id] = cd.team

        return driver_team_map

    def get_drivers_standings(
        self, first_race=None, last_race=None
    ) -> list[tuple[Driver, Team, int | Decimal]]:
        first_race = first_race or 0
        last_race = last_race or self.races.count()

        race_scores = [
            race.get_points()
            for race in self.races.all().prefetch_related("dna_entries", "race_entries")
        ]

        total_points: dict[int, int | Decimal] = defaultdict(int)
        player_finishes: dict[int, list[int | float]] = defaultdict(list)
        for race in race_scores:
            for driver, points in race["player_points"].items():
                total_points[driver] += points
            for driver, finish in race["player_finishes"].items():
                player_finishes[driver].append(finish)

        for (
            driver_id,
            penalty_points,
        ) in self.championshipdriver_set.all().values_list(
            "driver_id", "penalty_points"
        ):
            if driver_id not in total_points:
                total_points[driver_id] = 0
            # Penalty points
            total_points[driver_id] -= penalty_points

        for driver, _ in total_points.items():
            if len(player_finishes[driver]) == 0:
                player_finishes[driver] = [math.inf]
            else:
                player_finishes[driver] = sorted(player_finishes[driver])

        driver_team_map = self.get_driver_team_map()

        driver_map = {driver.id: driver for driver in Driver.objects.all()}

        total_points_list = [
            (driver_map[driver], driver_team_map[driver], points)
            for driver, points in total_points.items()
        ]

        total_points_list.sort(
            key=lambda item: (
                -item[2],
                player_finishes[item[0].id],
                item[1].name if item[1] else None,
                item[0].name,
            )
        )
        return total_points_list

    def get_constructors_standings(
        self, first_race=None, last_race=None
    ) -> list[tuple["Team", int | Decimal]]:
        first_race = first_race or 0
        last_race = last_race or self.races.count()

        team_scores: list[dict] = [
            race.get_points()
            for race in self.races.all().prefetch_related("dna_entries", "race_entries")
        ]

        driver_team_map = self.get_driver_team_map()

        total_points: dict[int, int | Decimal] = defaultdict(int)
        team_finishes: dict[int, list[int | float]] = defaultdict(list)
        for race in team_scores:
            for team, points in race["team_points"].items():
                if team:
                    total_points[team] += points
            for team, finishes in race["team_finishes"].items():
                team_finishes[team].extend(finishes)

        for driver_id, penalty_points in self.championshipdriver_set.all().values_list(
            "driver_id", "penalty_points"
        ):
            if (
                driver_team_map[driver_id]
                and driver_team_map[driver_id].id not in total_points
            ):
                total_points[driver_team_map[driver_id].id] = 0
            total_points[driver_team_map[driver_id].id] -= penalty_points

        for multiplier in self.multipliers.all():
            total_points[multiplier.constructor.id] *= Decimal(multiplier.multiplier)
            total_points[multiplier.constructor.id] -= multiplier.penalty_points

        for constructor_id, _ in total_points.items():
            if len(team_finishes[constructor_id]) == 0:
                team_finishes[constructor_id] = [math.inf]
            else:
                team_finishes[constructor_id] = sorted(team_finishes[constructor_id])

        team_map = {team.id: team for team in Team.objects.all()}

        total_points_list = [
            (team_map[team], points) for team, points in total_points.items()
        ]

        total_points_list.sort(
            key=lambda item: (-item[1], team_finishes[item[0].id], item[0].name)
        )

        return total_points_list

    class Meta:
        get_latest_by = "start_date"
        ordering = ("-start_date",)


class ChampionshipDriver(models.Model):
    championship = models.ForeignKey(Championship, on_delete=models.CASCADE)
    driver = models.ForeignKey(Driver, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.RESTRICT, blank=True, null=True)
    penalty_points = models.IntegerField(verbose_name="Penalty Points", default=0)


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

    driver_of_the_day = models.ForeignKey(
        Driver,
        on_delete=models.RESTRICT,
        related_name="driver_of_the_day_set",
        null=True,
        blank=True,
    )

    race_entries: QuerySet["RaceEntry"]
    dna_entries: QuerySet["DNAEntry"]

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

    def get_points(
        self,
    ) -> dict:
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
        dna_entries: list[RaceEntry] = list(self.dna_entries.all())
        entries: list[RaceEntry] = list(self.race_entries.all())
        player_entries = [entry for entry in entries if not entry.bot]
        bot_entries = [entry for entry in entries if entry.bot]

        num_entries = len(dna_entries) + len(player_entries)

        if num_entries == 0 or self.finished == False or len(entries) == 0:
            return {
                "player_points": {},
                "team_points": {},
                "player_finishes": {},
                "team_finishes": {},
            }

        # In Python
        # fastest_entry = None
        # fastest_time = None
        # for entry in entries:
        #     if fastest_time is None or (entry.best_lap_time is not None and entry.best_lap_time < fastest_time):
        #         fastest_entry = entry
        #         fastest_time = entry.best_lap_time
        try:
            fastest_entry = min(
                (entry for entry in entries if entry.best_lap_time is not None),
                key=lambda e: e.best_lap_time,
            )
        except ValueError:
            fastest_entry = entries[0]

        # Calculate Points
        total_points = {
            entry: SCORING_SYSTEM.get(entry.finish_position, 0) for entry in entries
        }

        # Fastest driver points
        if fastest_entry.finish_position <= 10:
            total_points[fastest_entry] += 1

        player_points: dict[int, int | Decimal] = {
            entry.driver_id: total_points[entry] for entry in player_entries
        }
        bot_points: list[int | Decimal] = [total_points[entry] for entry in bot_entries]

        # Distribute DNA points
        if len(dna_entries) > 0:
            # Sum of the first #DNA_ENTRIES bot scores
            total_bot_points = sum(sorted(bot_points, reverse=True)[: len(dna_entries)])
            dna_score = Decimal(total_bot_points) / Decimal(
                2 * len(dna_entries)
            )  # DNA Drivers receive half points
            dna_score = round(dna_score, 1)
            if dna_score > 0:
                for entry in dna_entries:
                    player_points[entry.driver_id] = dna_score
            else:
                for entry in dna_entries:
                    player_points[entry.driver_id] = 0

        cd_team_map = {
            driver_id: team
            for (
                driver_id,
                team,
            ) in self.championship.championshipdriver_set.all().values_list(
                "driver_id", "team"
            )
        }

        driver_team_map = {}

        # Calculate Team Scores
        team_points: dict[int, int | Decimal] = dict()

        for entry in chain(player_entries, dna_entries):
            if entry.team_id is not None:
                team = entry.team_id
                driver_team_map[entry.driver_id] = entry.team_id
            elif entry.driver_id in cd_team_map:
                team = cd_team_map[entry.driver_id]
                driver_team_map[entry.driver_id] = cd_team_map[entry.driver_id]
            elif entry.driver is not None and entry.driver.team is not None:
                team = entry.driver.team_id
                driver_team_map[entry.driver_id] = entry.driver.team_id
            else:
                continue
            team_points[team] = 0

        player_finishes = {}
        team_finishes = defaultdict(list)

        for entry in player_entries:
            player_finishes[entry.driver_id] = entry.finish_position
            if entry.driver_id in driver_team_map:
                team_finishes[driver_team_map[entry.driver_id]].append(
                    entry.finish_position
                )

        for entry in chain(player_entries, dna_entries):
            if entry.driver_id in driver_team_map:
                team_points[driver_team_map[entry.driver_id]] += player_points[
                    entry.driver_id
                ]

        return {
            "player_points": player_points,
            "team_points": team_points,
            "player_finishes": player_finishes,
            "team_finishes": team_finishes,
        }

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
            case _:
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

    def match_history(self) -> list[tuple["RaceEntry", int, "Team"]]:
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
        entries: QuerySet[RaceEntry] = self.race_entries.order_by(
            "finish_position"
        ).prefetch_related("driver", "team")

        fastest_entry: RaceEntry = self.fastest_lap()

        if self.finished == False:
            return []

        # Calculate Points
        total_points = {
            entry: SCORING_SYSTEM.get(entry.finish_position, 0) for entry in entries
        }

        # Fastest driver points
        if fastest_entry and fastest_entry.finish_position <= 10:
            total_points[fastest_entry] += 1

        team_map = {team.id: team for team in Team.objects.all()}

        cd_team_map = {
            driver_id: team
            for (
                driver_id,
                team,
            ) in self.championship.championshipdriver_set.all().values_list(
                "driver_id", "team"
            )
        }

        mh = []
        for entry in entries:
            if entry.team_id is not None:
                team = entry.team
            elif entry.driver_id in cd_team_map:
                team = team_map[cd_team_map[entry.driver_id]]
            elif entry.driver_id is not None:
                team = entry.driver.team
            else:
                team = None

            mh.append(
                (
                    entry,
                    total_points[entry],
                    team,
                )
            )

        return mh

    def fastest_lap(self) -> Optional["RaceEntry"]:
        entries = self.race_entries.all()
        fastest_entry = None
        if len(entries) > 0:
            try:
                fastest_entry = min(
                    (entry for entry in entries if entry.best_lap_time is not None),
                    key=lambda e: e.best_lap_time,
                )
            except ValueError:
                fastest_entry = entries[0]
        return fastest_entry

    class Meta:
        ordering = ("championship", "championship_order")


class RaceEntry(models.Model):
    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE,
        related_name="race_entries",
    )
    race_id: int
    driver = models.ForeignKey(
        Driver,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="race_entries",
    )
    driver_id: int
    team = models.ForeignKey(
        Team,
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="race_entries",
    )
    team_id: int

    bot = models.BooleanField(verbose_name="Is Bot", default=False)

    overtakes = models.IntegerField(
        verbose_name="Overtakes",
        validators=[MinValueValidator(0)],
        blank=True,
        null=True,
    )

    # Should be not null if not DNA
    qualifying_position = models.IntegerField(
        verbose_name="Qualifying Position",
        validators=[MinValueValidator(1)],
        blank=True,
        null=True,
    )
    grid_penalty = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    finish_position = models.IntegerField(
        validators=[MinValueValidator(1)],
    )

    best_lap_time = models.DurationField(null=True, blank=True)

    dnf = models.BooleanField(verbose_name="Did Not Finish", default=False)

    tires = models.CharField(max_length=32, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["race", "driver"], name="raceentry_unique_driver_race"
            ),
            models.UniqueConstraint(
                fields=["race", "qualifying_position"],
                name="raceentry_unique_driver_qualifying_position",
            ),
            models.UniqueConstraint(
                fields=["race", "finish_position"],
                name="raceentry_unique_driver_finish_position",
            ),
            models.CheckConstraint(
                check=(
                    Q(
                        bot=True,
                        driver__isnull=True,
                        team__isnull=True,
                    )
                    | Q(
                        bot=False,
                        driver__isnull=False,
                    )
                ),
                name="raceentry_dna_notnull",
            ),
        ]

        ordering = ("race", "finish_position")

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

    def __str__(self):
        return f"DNA: {self.driver}"

    class Meta:
        ordering = ("race",)


class RuleChapter(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=64)

    class Meta:
        ordering = ("number",)


class RuleEntry(models.Model):
    chapter = models.ForeignKey(
        RuleChapter, on_delete=models.RESTRICT, related_name="entries"
    )
    number = models.IntegerField()
    text = models.TextField()

    class Meta:
        ordering = ("chapter", "number")


class ConstructorMultiplier(models.Model):
    championship = models.ForeignKey(
        Championship, on_delete=models.CASCADE, related_name="multipliers"
    )
    constructor = models.ForeignKey(
        Team, on_delete=models.RESTRICT, related_name="multipliers"
    )
    multiplier = models.FloatField(default=1)
    penalty_points = models.IntegerField(default=0)

    class Meta:
        ordering = ("championship", "constructor")


class FAQ(models.Model):
    order = models.IntegerField()
    question = models.TextField()
    answer = models.TextField()

    class Meta:
        ordering = ("order",)
