import math
from time import perf_counter
from typing import Optional

from .models import Championship, Driver, Race, RaceEntry
from .util import timing


def average_int(l):
    s: int|float = 0
    c = 0
    for e in l:
        if isinstance(e, int|float):
            s += e
            c += 1
    if c > 0:
        return round(s/c)
    else:
        None

def average_float(l):
    s: int|float = 0
    c = 0
    for e in l:
        if isinstance(e, int|float):
            s += e
            c += 1
    if c > 0:
        return s/c
    else:
        None

def average_finish_position(l):
    s: int|float = 0
    c = 0
    for e in l:
        if e and not e.dnf and isinstance(e.finish_position, int|float):
            s += e.finish_position
            c += 1
    if c > 0:
        return round(s/c, 1)
    else:
        None

def average_quali_position(l):
    s: int|float = 0
    c = 0
    for e in l:
        if e and not e.dnf and isinstance(e.qualifying_position, int|float):
            s += e.qualifying_position
            c += 1
    if c > 0:
        return round(s/c, 1)
    else:
        None

def total_overtakes(l):
    s: int|float = 0

    for e in l:
        if e and isinstance(e.overtakes, int|float):
            s += e.overtakes
    
    return s
    


@timing
def stats_race_table(championship: Championship):    
    standings = championship.get_drivers_standings()

    races = list(championship.races.all().prefetch_related('race_entries', 'track', 'dna_entries')) # Also preload track for the html :)
    drivers = [driver for (driver, _, _) in standings]
    num_races = len(races)
    finish_dict: dict[int, list[Optional[RaceEntry]]] = {driver.id: [None]*num_races for driver in drivers}
    pace_dict: dict[int, list[Optional[int]]] = {driver.id: [None]*num_races for driver in drivers}
    best_race_result_dict: dict[int, Optional[RaceEntry]] = {driver.id: None for driver in drivers}
    best_quali_result_dict: dict[int, Optional[RaceEntry]] = {driver.id: None for driver in drivers}
    race_wins_dict: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_wins: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_wins_tmp: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_podiums: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_podiums_tmp: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_points: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_points_tmp: dict[int, int] = {driver.id: 0 for driver in drivers}

    most_consecutive_no_wins: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_no_wins_tmp: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_no_podiums: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_no_podiums_tmp: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_no_points: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_no_points_tmp: dict[int, int] = {driver.id: 0 for driver in drivers}

    most_consecutive_first_races: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_first_podiums: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_first_points: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_first_tmp: dict[int, bool] = {driver.id: True for driver in drivers}
    
    for i, race in enumerate(races):
        race: Race
        race_points_dict = race.get_points()
        points = race_points_dict['player_points']

        # Quali classification & Race classification
        # Best quali/race result
        for entry in race.race_entries.all():
            if entry.driver_id in finish_dict:
                finish_dict[entry.driver_id][i] = entry

                # Race
                if not entry.dnf:
                    best_race = best_race_result_dict[entry.driver_id]
                    if best_race is None or entry.finish_position < best_race.finish_position:
                        best_race_result_dict[entry.driver_id] = entry
                    
                # Quali
                best_quali = best_quali_result_dict[entry.driver_id]
                if best_quali is None or entry.qualifying_position < best_quali.qualifying_position:
                    best_quali_result_dict[entry.driver_id] = entry

                # Wins
                if entry.finish_position == 1:
                    race_wins_dict[entry.driver_id] += 1

                # consecutive with
                if entry.finish_position == 1:
                    most_consecutive_wins_tmp[entry.driver_id] += 1
                else:
                    if most_consecutive_wins_tmp[entry.driver_id] > most_consecutive_wins[entry.driver_id]:
                        most_consecutive_wins[entry.driver_id] = most_consecutive_wins_tmp[entry.driver_id]
                    most_consecutive_wins_tmp[entry.driver_id] = 0
                
                if entry.finish_position <= 3:
                    most_consecutive_podiums_tmp[entry.driver_id] += 1
                else:
                    if most_consecutive_podiums_tmp[entry.driver_id] > most_consecutive_podiums[entry.driver_id]:
                        most_consecutive_podiums[entry.driver_id] = most_consecutive_podiums_tmp[entry.driver_id]
                    most_consecutive_podiums_tmp[entry.driver_id] = 0

                if entry.finish_position <= 10:
                    most_consecutive_points_tmp[entry.driver_id] += 1
                else:
                    if most_consecutive_points_tmp[entry.driver_id] > most_consecutive_points[entry.driver_id]:
                        most_consecutive_points[entry.driver_id] = most_consecutive_points_tmp[entry.driver_id]
                    most_consecutive_points_tmp[entry.driver_id] = 0

                # Consecutive without
                if entry.finish_position == 1:
                    if most_consecutive_no_wins_tmp[entry.driver_id] > most_consecutive_no_wins[entry.driver_id]:
                        most_consecutive_no_wins[entry.driver_id] = most_consecutive_no_wins_tmp[entry.driver_id]
                    most_consecutive_no_wins_tmp[entry.driver_id] = 0

                    if most_consecutive_no_podiums_tmp[entry.driver_id] > most_consecutive_no_podiums[entry.driver_id]:
                        most_consecutive_no_podiums[entry.driver_id] = most_consecutive_no_podiums_tmp[entry.driver_id]
                    most_consecutive_no_podiums_tmp[entry.driver_id] = 0

                    if most_consecutive_no_points_tmp[entry.driver_id] > most_consecutive_no_points[entry.driver_id]:
                        most_consecutive_no_points[entry.driver_id] = most_consecutive_no_points_tmp[entry.driver_id]
                    most_consecutive_no_points_tmp[entry.driver_id] = 0
                else:
                    if entry.finish_position <= 3:
                        most_consecutive_no_podiums_tmp[entry.driver_id] += 1

                    most_consecutive_no_points_tmp[entry.driver_id] += points[entry.driver_id]

                    most_consecutive_no_wins_tmp[entry.driver_id] += 1

                # Before first win
                if entry.finish_position == 1:
                    most_consecutive_first_tmp[entry.driver_id] = False
                elif most_consecutive_first_tmp[entry.driver_id]:
                    if entry.finish_position <= 3:
                        most_consecutive_first_podiums[entry.driver_id] += 1

                    most_consecutive_first_points[entry.driver_id] += points[entry.driver_id]

                    most_consecutive_first_races[entry.driver_id] += 1

                        

        # Pace
        fastest_lap = race.fastest_lap()
        if fastest_lap is None:
            continue

        fastest_lap_field = fastest_lap.best_lap_time
        if fastest_lap_field is None:
            continue
        fastest_lap: float = fastest_lap_field.total_seconds()

        def score(laptime):
            return 100*(fastest_lap/(18*(laptime-fastest_lap) + fastest_lap))

        entries = race.race_entries.all()
        for entry in entries:
            if entry.driver_id and not entry.dnf and entry.best_lap_time is not None:
                pace = score(entry.best_lap_time.total_seconds())
                pace_dict[entry.driver_id][i] = round(pace)

    # With
    for driver_id, streak in most_consecutive_wins_tmp.items():
        if streak > most_consecutive_wins[driver_id]:
            most_consecutive_wins[driver_id] = streak

    for driver_id, streak in most_consecutive_podiums_tmp.items():
        if streak > most_consecutive_podiums[driver_id]:
            most_consecutive_podiums[driver_id] = streak

    for driver_id, streak in most_consecutive_points_tmp.items():
        if streak > most_consecutive_points[driver_id]:
            most_consecutive_points[driver_id] = streak

    # Without
    for driver_id, streak in most_consecutive_no_wins_tmp.items():
        if streak > most_consecutive_no_wins[driver_id]:
            most_consecutive_no_wins[driver_id] = streak

    for driver_id, streak in most_consecutive_no_podiums_tmp.items():
        if streak > most_consecutive_no_podiums[driver_id]:
            most_consecutive_no_podiums[driver_id] = streak

    for driver_id, streak in most_consecutive_no_points_tmp.items():
        if streak > most_consecutive_no_points[driver_id]:
            most_consecutive_no_points[driver_id] = streak


    race_wins_unique = sorted(list(set(race_wins_dict.values())), reverse=True)
    
    most_consecutive_wins_unique = sorted(list(set(most_consecutive_wins.values())), reverse=True)
    most_consecutive_podiums_unique = sorted(list(set(most_consecutive_podiums.values())), reverse=True)
    most_consecutive_points_unique = sorted(list(set(most_consecutive_points.values())), reverse=True)

    most_consecutive_no_wins_unique = sorted(list(set(most_consecutive_no_wins.values())), reverse=True)
    most_consecutive_no_podiums_unique = sorted(list(set(most_consecutive_no_podiums.values())), reverse=True)
    most_consecutive_no_points_unique = sorted(list(set(most_consecutive_no_points.values())), reverse=True)

    most_consecutive_first_races_unique = sorted(list(set(most_consecutive_first_races.values())), reverse=True)
    most_consecutive_first_podiums_unique = sorted(list(set(most_consecutive_first_podiums.values())), reverse=True)
    most_consecutive_first_points_unique = sorted(list(set(most_consecutive_first_points.values())), reverse=True)

    stats_table = (
        races,
        {
            "results": [{
                    "driver": driver,
                    "entries": finish_dict[driver.id],
                    "average_finish": average_finish_position(finish_dict[driver.id]),
                    "average_quali": average_quali_position(finish_dict[driver.id]),
                } for driver in drivers],
            
            "overtakes": sorted([{
                "driver": driver,
                "entries": finish_dict[driver.id],
                "total_overtakes": total_overtakes(finish_dict[driver.id]),
            } for driver in drivers], key=lambda e: e["total_overtakes"], reverse=True),
            
            "best_results": sorted([(driver, best_race_result_dict[driver.id], best_quali_result_dict[driver.id]) for driver in drivers], key=lambda e: (e[1].finish_position if e[1] else math.inf, e[2].qualifying_position if e[2] else math.inf)),

            "race_wins": {
                "entries": sorted([(driver, race_wins_dict[driver.id]) for driver in drivers], key=lambda e: e[1], reverse=True),
                "first": race_wins_unique[0] if len(race_wins_unique) > 0 else None,
                "second": race_wins_unique[1] if len(race_wins_unique) > 1 else None,
                "third": race_wins_unique[2] if len(race_wins_unique) > 2 else None,
            },

            "pace": sorted(
                [{"driver": driver, "entries": pace_dict[driver.id], "average": average_int(pace_dict[driver.id])} for driver in drivers],
                key= lambda e: e["average"] or -math.inf, reverse=True
            ),

            "consecutive": sorted([
                {
                    "driver": driver,
                    "wins": {
                        "value": most_consecutive_wins[driver.id],
                        "first": most_consecutive_wins_unique[0] if len(most_consecutive_wins_unique) > 0 else None,
                        "second": most_consecutive_wins_unique[1] if len(most_consecutive_wins_unique) > 1 else None,
                        "third": most_consecutive_wins_unique[2] if len(most_consecutive_wins_unique) > 2 else None,
                        },
                    "podiums": {
                        "value": most_consecutive_podiums[driver.id],
                        "first": most_consecutive_podiums_unique[0] if len(most_consecutive_podiums_unique) > 0 else None,
                        "second": most_consecutive_podiums_unique[1] if len(most_consecutive_podiums_unique) > 1 else None,
                        "third": most_consecutive_podiums_unique[2] if len(most_consecutive_podiums_unique) > 2 else None,
                        },
                    "points": {
                        "value": most_consecutive_points[driver.id],
                        "first": most_consecutive_points_unique[0] if len(most_consecutive_points_unique) > 0 else None,
                        "second": most_consecutive_points_unique[1] if len(most_consecutive_points_unique) > 1 else None,
                        "third": most_consecutive_points_unique[2] if len(most_consecutive_points_unique) > 2 else None,
                        },
                } for driver in drivers
            ],
            key=lambda e: (e["wins"]["value"], e["podiums"]["value"], e["points"]["value"]),
            reverse=True),

            "consecutive_without": sorted([
                {
                    "driver": driver,
                    "wins": {
                        "value": most_consecutive_no_wins[driver.id],
                        "first": most_consecutive_no_wins_unique[0] if len(most_consecutive_no_wins_unique) > 0 else None,
                        "second": most_consecutive_no_wins_unique[1] if len(most_consecutive_no_wins_unique) > 1 else None,
                        "third": most_consecutive_no_wins_unique[2] if len(most_consecutive_no_wins_unique) > 2 else None,
                        },
                    "podiums": {
                        "value": most_consecutive_no_podiums[driver.id],
                        "first": most_consecutive_no_podiums_unique[0] if len(most_consecutive_no_podiums_unique) > 0 else None,
                        "second": most_consecutive_no_podiums_unique[1] if len(most_consecutive_no_podiums_unique) > 1 else None,
                        "third": most_consecutive_no_podiums_unique[2] if len(most_consecutive_no_podiums_unique) > 2 else None,
                        },
                    "points": {
                        "value": most_consecutive_no_points[driver.id],
                        "first": most_consecutive_no_points_unique[0] if len(most_consecutive_no_points_unique) > 0 else None,
                        "second": most_consecutive_no_points_unique[1] if len(most_consecutive_no_points_unique) > 1 else None,
                        "third": most_consecutive_no_points_unique[2] if len(most_consecutive_no_points_unique) > 2 else None,
                        },
                } for driver in drivers
            ],
            key=lambda e: (e["podiums"]["value"], e["points"]["value"], e["wins"]["value"]),
            reverse=True),

            "before_first_win": sorted([
                {
                    "driver": driver,
                    "races": {
                        "value": most_consecutive_first_races[driver.id],
                        "first": most_consecutive_first_races_unique[0] if len(most_consecutive_first_races_unique) > 0 else None,
                        "second": most_consecutive_first_races_unique[1] if len(most_consecutive_first_races_unique) > 1 else None,
                        "third": most_consecutive_first_races_unique[2] if len(most_consecutive_first_races_unique) > 2 else None,
                        },
                    "podiums": {
                        "value": most_consecutive_first_podiums[driver.id],
                        "first": most_consecutive_first_podiums_unique[0] if len(most_consecutive_first_podiums_unique) > 0 else None,
                        "second": most_consecutive_first_podiums_unique[1] if len(most_consecutive_first_podiums_unique) > 1 else None,
                        "third": most_consecutive_first_podiums_unique[2] if len(most_consecutive_first_podiums_unique) > 2 else None,
                        },
                    "points": {
                        "value": most_consecutive_first_points[driver.id],
                        "first": most_consecutive_first_points_unique[0] if len(most_consecutive_first_points_unique) > 0 else None,
                        "second": most_consecutive_first_points_unique[1] if len(most_consecutive_first_points_unique) > 1 else None,
                        "third": most_consecutive_first_points_unique[2] if len(most_consecutive_first_points_unique) > 2 else None,
                        },
                } for driver in drivers
            ],
            key=lambda e: (e["podiums"]["value"], e["points"]["value"], e["races"]["value"]),
            reverse=True)
        }
    )
    return stats_table
