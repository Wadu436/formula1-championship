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

@timing
def stats_race_table(championship: Championship):    
    standings = championship.get_drivers_standings()

    races = list(championship.races.all().prefetch_related('race_entries', 'track')) # Also preload track for the html :)
    drivers = [driver for (driver, _, _) in standings]
    num_races = len(races)
    finish_dict: dict[int, list[Optional[RaceEntry]]] = {driver.id: [None]*num_races for driver in drivers}
    pace_dict: dict[int, list[Optional[int]]] = {driver.id: [None]*num_races for driver in drivers}

    for i, race in enumerate(races):
        race: Race

        # Quali classification & Race classification
        for entry in race.race_entries.all():
            if entry.driver_id in finish_dict:
                finish_dict[entry.driver_id][i] = entry

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

        # Best result



    finish_table = (races, [
        (driver, {
            "entries": finish_dict[driver.id], 
            "pace": pace_dict[driver.id], 
            "average_finish": average_finish_position(finish_dict[driver.id]), 
            "average_quali": average_quali_position(finish_dict[driver.id]), 
            "average_pace": average_int(pace_dict[driver.id])
            }
            ) for driver in drivers
            ])

    return finish_table
