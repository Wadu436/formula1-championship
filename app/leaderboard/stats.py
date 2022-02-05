from datetime import timedelta

from .models import Championship, Driver, Race, RaceEntry


def average(l):
    s = 0
    c = 0
    nn = False
    for e in l:
        if e is not None:
            nn = True
            s += e
            c += 1
    if nn:
        return int(s/c)
    else:
        None

def stats_pace(championship: Championship):
    standings = championship.get_drivers_standings()
    drivers = [driver for (driver, _, _) in standings]
    races = championship.races.all()
    num_races = championship.races.count()

    pace_dict = {driver: [None]*num_races for driver in drivers}

    for i, race in enumerate(races):
        race: Race
        if race.fastest_lap() is None:
            continue

        fastest_lap_field = race.fastest_lap().best_lap_time
        if fastest_lap_field is None:
            continue
        fastest_lap: float = fastest_lap_field.total_seconds()

        def score(laptime):
            return (100*fastest_lap)/(18*(laptime-fastest_lap) + fastest_lap)

        entries = race.race_entries.all()
        for entry in entries:
            if not entry.dnf and entry.best_lap_time:
                pace = score(entry.best_lap_time.total_seconds())
                if entry.driver:
                    pace_dict[entry.driver][i] = int(pace)

    pace_table = (races, [(driver, pace_dict[driver], average(pace_dict[driver])) for driver in drivers])
    print(pace_table)

    return pace_table
