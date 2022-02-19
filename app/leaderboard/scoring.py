import math
from collections import defaultdict
from decimal import Decimal
from itertools import chain

from django.db.models.query import QuerySet

from .models import Championship, DNAEntry, Driver, Race, RaceEntry, Team


def race_points(
    race: Race,
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
    dna_entries: list[DNAEntry] = list(race.dna_entries.all().prefetch_related("team"))
    entries: list[RaceEntry] = list(race.race_entries.all().prefetch_related("team"))
    player_entries = [entry for entry in entries if not entry.bot]
    bot_entries = [entry for entry in entries if entry.bot]

    num_entries = len(dna_entries) + len(player_entries)

    if num_entries == 0 or race.finished == False or len(entries) == 0:
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

    driver_team_map = race.championship.get_driver_team_map()

    # Calculate Team Scores
    team_points: dict[int, int | Decimal] = defaultdict(int)

    for entry in chain(player_entries, dna_entries):
        if entry.team_id is not None:
            driver_team_map[entry.driver_id] = entry.team

    player_finishes = {}
    team_finishes = defaultdict(list)

    for entry in player_entries:
        player_finishes[entry.driver_id] = entry.finish_position
        if entry.driver_id in driver_team_map:
            team_finishes[driver_team_map[entry.driver_id].id].append(
                entry.finish_position
            )

    for entry in chain(player_entries, dna_entries):
        if entry.driver_id in driver_team_map:
            team_points[driver_team_map[entry.driver_id].id] += player_points[
                entry.driver_id
            ]

    return {
        "player_points": player_points,
        "team_points": team_points,
        "player_finishes": player_finishes,
        "team_finishes": team_finishes,
    }


def _drivers_standings_list(championship, race_scores):
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
    ) in championship.championshipdriver_set.all().values_list(
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

    driver_team_map = championship.get_driver_team_map()

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


def drivers_standings(
    championship: Championship,
) -> list[tuple[Driver, Team, int | Decimal, int]]:
    races = championship.races.filter(finished=True)

    race_scores = [
        race_points(race)
        for race in races.order_by("championship_order").prefetch_related(
            "dna_entries", "race_entries"
        )
    ]

    current_ranking = _drivers_standings_list(championship, race_scores)
    prev_ranking = _drivers_standings_list(
        championship, race_scores[:-1] if len(races) > 0 else race_scores
    )

    this_rank = {driver: i for i, (driver, _, _) in enumerate(current_ranking)}
    prev_rank = {driver: i for i, (driver, _, _) in enumerate(prev_ranking)}

    # (Driver, team, points, delta)
    ranking = [
        (
            driver,
            team,
            points,
            this_rank[driver] - prev_rank[driver]
            if driver in this_rank and driver in prev_rank and len(races) > 1
            else 0,
        )
        for driver, team, points in current_ranking
    ]

    return ranking


def _constructors_standings_list(
    championship: Championship, race_scores
) -> list[tuple["Team", int | Decimal]]:
    driver_team_map = championship.get_driver_team_map()

    total_points: dict[int, int | Decimal] = defaultdict(int)
    team_finishes: dict[int, list[int | float]] = defaultdict(list)
    for race in race_scores:
        for team, points in race["team_points"].items():
            if team:
                total_points[team] += points
        for team, finishes in race["team_finishes"].items():
            team_finishes[team].extend(finishes)

    for (
        driver_id,
        penalty_points,
    ) in championship.championshipdriver_set.all().values_list(
        "driver_id", "penalty_points"
    ):
        total_points[driver_team_map[driver_id].id] -= penalty_points

    for multiplier in championship.multipliers.all():
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


def constructors_standings(
    championship: Championship, first_race=None, last_race=None
) -> list[tuple["Team", int | Decimal, int]]:
    races = championship.races.filter(finished=True)

    race_scores = [
        race_points(race)
        for race in races.order_by("championship_order").prefetch_related(
            "dna_entries", "race_entries"
        )
    ]

    current_ranking = _constructors_standings_list(championship, race_scores)
    prev_ranking = _constructors_standings_list(
        championship, race_scores[:-1] if len(races) > 0 else race_scores
    )

    this_rank = {team: i for i, (team, _) in enumerate(current_ranking)}
    prev_rank = {team: i for i, (team, _) in enumerate(prev_ranking)}

    # (Driver, team, points, delta)
    ranking = [
        (
            team,
            points,
            this_rank[team] - prev_rank[team]
            if team in this_rank and team in prev_rank and len(races) > 1
            else 0,
        )
        for team, points in current_ranking
    ]

    return ranking


def match_history(race: Race) -> list[tuple["RaceEntry", int, "Team"]]:
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
    entries: QuerySet[RaceEntry] = race.race_entries.order_by(
        "finish_position"
    ).prefetch_related("driver", "team")

    fastest_entry: RaceEntry | None = race.fastest_lap()

    if race.finished == False:
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
        ) in race.championship.championshipdriver_set.all().values_list(
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
