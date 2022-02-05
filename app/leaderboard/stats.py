from time import perf_counter
from typing import Optional

from .models import Championship, Driver, Race, RaceEntry
from .util import timing


def average_int(l):
    s: int|float = 0
    c = 0
    nn = False
    for e in l:
        if isinstance(e, int|float):
            nn = True
            s += e
            c += 1
    if nn:
        return int(s/c)
    else:
        None

def average_float(l):
    s: int|float = 0
    c = 0
    nn = False
    for e in l:
        if isinstance(e, int|float):
            nn = True
            s += e
            c += 1
    if nn:
        return s/c
    else:
        None

def average_finish_position(l):
    s: int|float = 0
    c = 0
    nn = False
    for e in l:
        if e and not e.dnf and isinstance(e.finish_position, int|float):
            nn = True
            s += e.finish_position
            c += 1
    if nn:
        return round(s/c, 1)
    else:
        None

@timing
def stats_race_table(championship: Championship):
    a = perf_counter()
    # A
    standings = championship.get_drivers_standings()

    b = perf_counter()
    # B
    races = list(championship.races.all().prefetch_related('race_entries', 'track')) # Also preload track for the html :)
    drivers = [driver for (driver, _, _) in standings]
    num_races = len(races)
    finish_dict: dict[int, list[Optional[RaceEntry]]] = {driver.id: [None]*num_races for driver in drivers}
    pace_dict: dict[int, list[Optional[int]]] = {driver.id: [None]*num_races for driver in drivers}

    c = perf_counter()
    # C
    for i, race in enumerate(races):
        for entry in race.race_entries.all():
            if entry.driver_id in finish_dict:
                finish_dict[entry.driver_id][i] = entry

        race: Race
        fastest_lap = race.fastest_lap()
        if fastest_lap is None:
            continue

        fastest_lap_field = fastest_lap.best_lap_time
        if fastest_lap_field is None:
            continue
        fastest_lap: float = fastest_lap_field.total_seconds()

        def score(laptime):
            return (100*fastest_lap)/(18*(laptime-fastest_lap) + fastest_lap)

        entries = race.race_entries.all()
        for entry in entries:
            if entry.driver_id and not entry.dnf and entry.best_lap_time:
                pace = score(entry.best_lap_time.total_seconds())
                pace_dict[entry.driver_id][i] = int(pace)

    d = perf_counter()
    # D
    finish_table = (races, [(driver, {"entries": finish_dict[driver.id], "pace": pace_dict[driver.id], "average_finish": average_finish_position(finish_dict[driver.id]), "average_pace": average_int(pace_dict[driver.id])}) for driver in drivers])

    e = perf_counter()

    print(f"""A: {b-a}
    B: {c-b}
    C: {d-c}
    D: {e-d}""")

    return finish_table
