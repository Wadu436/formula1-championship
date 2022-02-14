import math
from time import perf_counter
from typing import Optional

from .models import Championship, Race, RaceEntry
from .scoring import drivers_standings, race_points
from .util import timing


def average_int(l):
    s: int | float = 0
    c = 0
    for e in l:
        if isinstance(e, int | float):
            s += e
            c += 1
    if c > 0:
        return round(s / c)
    else:
        None


def average_float(l):
    s: int | float = 0
    c = 0
    for e in l:
        if isinstance(e, int | float):
            s += e
            c += 1
    if c > 0:
        return s / c
    else:
        None


def average_finish_position(l):
    s: int | float = 0
    c = 0
    for e in l:
        if e and not e.dnf and isinstance(e.finish_position, int | float):
            s += e.finish_position
            c += 1
    if c > 0:
        rnd = round(s / c, 1)
        if rnd % 1 == 0:
            return int(rnd)
        return rnd
    else:
        None


def average_quali_position(l):
    s: int | float = 0
    c = 0
    for e in l:
        if e and isinstance(e.qualifying_position, int | float):
            s += e.qualifying_position
            c += 1
    if c > 0:
        rnd = round(s / c, 1)
        if rnd % 1 == 0:
            return int(rnd)
        return rnd
    else:
        None


def total_overtakes(l):
    s: int | float = 0

    for e in l:
        if e and isinstance(e.overtakes, int | float):
            s += e.overtakes

    return s


def hex_to_rgb(value):
    value = value.lstrip("#")
    return tuple(int(value[2 * i : 2 * i + 2], 16) for i in range(0, 3))


def rgb_to_hex(rgb):
    r, g, b = rgb
    return f"#{r:02x}{g:02x}{b:02x}"


def three_point_gradient(start, mid, end, val):
    mid_r, mid_g, mid_b = hex_to_rgb(mid)
    val = min(max(val, 0), 1)
    if val < 0.5:
        start_r, start_g, start_b = hex_to_rgb(start)
        alpha = 2 * (0.5 - val)

        mix_r = alpha * start_r + (1 - alpha) * mid_r
        mix_g = alpha * start_g + (1 - alpha) * mid_g
        mix_b = alpha * start_b + (1 - alpha) * mid_b
    else:
        end_r, end_g, end_b = hex_to_rgb(end)
        alpha = 2 * (val - 0.5)

        mix_r = alpha * end_r + (1 - alpha) * mid_r
        mix_g = alpha * end_g + (1 - alpha) * mid_g
        mix_b = alpha * end_b + (1 - alpha) * mid_b

    return rgb_to_hex((int(mix_r), int(mix_g), int(mix_b)))


@timing
def stats_race_table(championship: Championship):
    standings = drivers_standings(championship)

    races = list(
        championship.races.all().prefetch_related(
            "race_entries", "track", "dna_entries"
        )
    )  # Also preload track for the html :)
    drivers = [driver for (driver, _, _) in standings]
    num_races = len(races)
    finish_dict: dict[int, list[Optional[RaceEntry]]] = {
        driver.id: [None] * num_races for driver in drivers
    }
    pace_dict: dict[int, list[Optional[int]]] = {
        driver.id: [None] * num_races for driver in drivers
    }
    best_race_result_dict: dict[int, Optional[RaceEntry]] = {
        driver.id: None for driver in drivers
    }
    best_quali_result_dict: dict[int, Optional[RaceEntry]] = {
        driver.id: None for driver in drivers
    }
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
    most_consecutive_no_podiums_tmp: dict[int, int] = {
        driver.id: 0 for driver in drivers
    }
    most_consecutive_no_points: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_no_points_tmp: dict[int, int] = {
        driver.id: 0 for driver in drivers
    }

    most_consecutive_first_races: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_first_podiums: dict[int, int] = {
        driver.id: 0 for driver in drivers
    }
    most_consecutive_first_points: dict[int, int] = {driver.id: 0 for driver in drivers}
    most_consecutive_first_tmp: dict[int, bool] = {
        driver.id: True for driver in drivers
    }

    for i, race in enumerate(races):
        race: Race
        race_points_dict = race_points(race)
        points = race_points_dict["player_points"]

        # Quali classification & Race classification
        # Best quali/race result
        for entry in race.race_entries.all():
            if entry.driver_id in finish_dict:
                finish_dict[entry.driver_id][i] = entry

                # Race
                if not entry.dnf:
                    best_race = best_race_result_dict[entry.driver_id]
                    if (
                        best_race is None
                        or entry.finish_position < best_race.finish_position
                    ):
                        best_race_result_dict[entry.driver_id] = entry

                # Quali
                best_quali = best_quali_result_dict[entry.driver_id]
                if best_quali is None or (
                    entry.qualifying_position is not None
                    and entry.qualifying_position < best_quali.qualifying_position
                ):
                    best_quali_result_dict[entry.driver_id] = entry

                # Wins
                if entry.finish_position == 1:
                    race_wins_dict[entry.driver_id] += 1

                # consecutive with
                if entry.finish_position == 1:
                    most_consecutive_wins_tmp[entry.driver_id] += 1
                else:
                    if (
                        most_consecutive_wins_tmp[entry.driver_id]
                        > most_consecutive_wins[entry.driver_id]
                    ):
                        most_consecutive_wins[
                            entry.driver_id
                        ] = most_consecutive_wins_tmp[entry.driver_id]
                    most_consecutive_wins_tmp[entry.driver_id] = 0

                if entry.finish_position <= 3:
                    most_consecutive_podiums_tmp[entry.driver_id] += 1
                else:
                    if (
                        most_consecutive_podiums_tmp[entry.driver_id]
                        > most_consecutive_podiums[entry.driver_id]
                    ):
                        most_consecutive_podiums[
                            entry.driver_id
                        ] = most_consecutive_podiums_tmp[entry.driver_id]
                    most_consecutive_podiums_tmp[entry.driver_id] = 0

                if entry.finish_position <= 10:
                    most_consecutive_points_tmp[entry.driver_id] += 1
                else:
                    if (
                        most_consecutive_points_tmp[entry.driver_id]
                        > most_consecutive_points[entry.driver_id]
                    ):
                        most_consecutive_points[
                            entry.driver_id
                        ] = most_consecutive_points_tmp[entry.driver_id]
                    most_consecutive_points_tmp[entry.driver_id] = 0

                # Consecutive without
                if entry.finish_position == 1:
                    if (
                        most_consecutive_no_wins_tmp[entry.driver_id]
                        > most_consecutive_no_wins[entry.driver_id]
                    ):
                        most_consecutive_no_wins[
                            entry.driver_id
                        ] = most_consecutive_no_wins_tmp[entry.driver_id]
                    most_consecutive_no_wins_tmp[entry.driver_id] = 0

                    if (
                        most_consecutive_no_podiums_tmp[entry.driver_id]
                        > most_consecutive_no_podiums[entry.driver_id]
                    ):
                        most_consecutive_no_podiums[
                            entry.driver_id
                        ] = most_consecutive_no_podiums_tmp[entry.driver_id]
                    most_consecutive_no_podiums_tmp[entry.driver_id] = 0

                    if (
                        most_consecutive_no_points_tmp[entry.driver_id]
                        > most_consecutive_no_points[entry.driver_id]
                    ):
                        most_consecutive_no_points[
                            entry.driver_id
                        ] = most_consecutive_no_points_tmp[entry.driver_id]
                    most_consecutive_no_points_tmp[entry.driver_id] = 0
                else:
                    if entry.finish_position <= 3:
                        most_consecutive_no_podiums_tmp[entry.driver_id] += 1

                    most_consecutive_no_points_tmp[entry.driver_id] += points[
                        entry.driver_id
                    ]

                    most_consecutive_no_wins_tmp[entry.driver_id] += 1

                # Before first win
                if entry.finish_position == 1:
                    most_consecutive_first_tmp[entry.driver_id] = False
                elif most_consecutive_first_tmp[entry.driver_id]:
                    if entry.finish_position <= 3:
                        most_consecutive_first_podiums[entry.driver_id] += 1

                    most_consecutive_first_points[entry.driver_id] += points[
                        entry.driver_id
                    ]

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
            return 100 * (fastest_lap / (18 * (laptime - fastest_lap) + fastest_lap))

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

    most_consecutive_wins_unique = sorted(
        list(set(most_consecutive_wins.values())), reverse=True
    )
    most_consecutive_podiums_unique = sorted(
        list(set(most_consecutive_podiums.values())), reverse=True
    )
    most_consecutive_points_unique = sorted(
        list(set(most_consecutive_points.values())), reverse=True
    )

    most_consecutive_no_wins_unique = sorted(
        list(set(most_consecutive_no_wins.values())), reverse=True
    )
    most_consecutive_no_podiums_unique = sorted(
        list(set(most_consecutive_no_podiums.values())), reverse=True
    )
    most_consecutive_no_points_unique = sorted(
        list(set(most_consecutive_no_points.values())), reverse=True
    )

    most_consecutive_first_races_unique = sorted(
        list(set(most_consecutive_first_races.values())), reverse=True
    )
    most_consecutive_first_podiums_unique = sorted(
        list(set(most_consecutive_first_podiums.values())), reverse=True
    )
    most_consecutive_first_points_unique = sorted(
        list(set(most_consecutive_first_points.values())), reverse=True
    )

    def finish_position_colors(pos):
        match pos:
            case 1:
                color = None
                bg_color = "gold"
            case 2:
                color = None
                bg_color = "silver"
            case 3:
                color = None
                color = "white"
                bg_color = "#cd7f32"
            case num if num <= 10:
                color = None
                bg_color = "#d1f3c5"
            case _:
                color = "white"
                bg_color = "gray"

        return (color, bg_color)

    def avg_finish_position_colors(pos):
        if pos is None:
            return (None, "lightgray")
        match pos:
            case num if num < 2:
                color = None
                bg_color = "gold"
            case num if num < 3:
                color = None
                bg_color = "silver"
            case num if num < 4:
                color = None
                color = "white"
                bg_color = "#cd7f32"
            case num if num < 11:
                color = None
                bg_color = "#d1f3c5"
            case _:
                color = "white"
                bg_color = "gray"

        return (color, bg_color)

    def pace_colors(pace):
        OFFSET = 0.1
        return (
            None,
            three_point_gradient(
                "#e67c73", "#ffd666", "#57bb8a", (pace / 100 - OFFSET) / (1 - OFFSET)
            ),
        )

    def overtake_colors(pace):
        OFFSET = 0.0
        return (
            None,
            three_point_gradient(
                "#e67c73", "#ffd666", "#57bb8a", (pace / 10 - OFFSET) / (1 - OFFSET)
            ),
        )

    def total_overtake_colors(pace):
        OFFSET = 0.0
        return (
            None,
            three_point_gradient(
                "#e67c73", "#ffd666", "#57bb8a", (pace / 150 - OFFSET) / (1 - OFFSET)
            ),
        )

    def init_table(races, final_column):
        return {
            "head": [{"value": ""}, {"value": "Driver"}]
            + [
                {"value": race.track.abbreviation, "class": "stats-centered"}
                for race in races
            ]
            + [{"value": final_column, "class": "stats-centered"}],
            "rows": [],
        }

    # Race classification table
    race_classification_table = init_table(races=races, final_column="Avg")

    for i, driver in enumerate(drivers):
        row = []
        row.append({"value": i + 1, "class": "stats-padded"})
        row.append({"value": driver.name, "class": "stats-padded"})
        for entry in finish_dict[driver.id]:
            if entry is None:
                value = "-"
                color = None
                bg_color = "lightgray"
            elif entry.dnf:
                value = "DNF"
                color = "white"
                bg_color = "#15151d"
            else:
                value = entry.finish_position
                color, bg_color = finish_position_colors(entry.finish_position)

            row.append(
                {
                    "value": value,
                    "class": "stats-centered",
                    "color": color,
                    "bg_color": bg_color,
                }
            )
        avg = average_finish_position(finish_dict[driver.id])
        avg_color, avg_bg_color = avg_finish_position_colors(avg)
        row.append(
            {
                "value": avg if avg is not None else "-",
                "class": "stats-centered",
                "color": avg_color,
                "bg_color": avg_bg_color,
            }
        )
        race_classification_table["rows"].append(
            {"row": row, "key": (avg if avg is not None else math.inf, driver.name)}
        )

    race_classification_table["rows"].sort(key=lambda row: row["key"])

    # Quali classification table
    quali_classification_table = init_table(races=races, final_column="Avg")

    for i, driver in enumerate(drivers):
        row = []
        row.append({"value": i + 1, "class": "stats-padded"})
        row.append({"value": driver.name, "class": "stats-padded"})
        for entry in finish_dict[driver.id]:
            if entry is None or entry.qualifying_position is None:
                value = "-"
                color = None
                bg_color = "lightgray"
            else:
                value = entry.qualifying_position
                color, bg_color = finish_position_colors(entry.qualifying_position)

            row.append(
                {
                    "value": value,
                    "class": "stats-centered",
                    "color": color,
                    "bg_color": bg_color,
                }
            )
        avg = average_quali_position(finish_dict[driver.id])
        avg_color, avg_bg_color = avg_finish_position_colors(avg)
        row.append(
            {
                "value": avg if avg is not None else "-",
                "class": "stats-centered",
                "color": avg_color,
                "bg_color": avg_bg_color,
            }
        )
        quali_classification_table["rows"].append(
            {"row": row, "key": (avg if avg is not None else math.inf, driver.name)}
        )

    quali_classification_table["rows"].sort(key=lambda row: row["key"])

    # Pace table
    pace_table = init_table(races=races, final_column="Avg")

    for driver in drivers:
        row = []
        row.append({"value": 0, "class": "stats-padded"})
        row.append({"value": driver.name, "class": "stats-padded"})
        for pace in pace_dict[driver.id]:
            if pace is None:
                value = "-"
                color = None
                bg_color = "lightgray"
            else:
                value = pace
                color, bg_color = pace_colors(pace)

            row.append(
                {
                    "value": value,
                    "class": "stats-centered",
                    "color": color,
                    "bg_color": bg_color,
                }
            )
        avg = average_int(pace_dict[driver.id])
        if avg:
            avg_color, avg_bg_color = pace_colors(avg)
        else:
            avg_color = None
            avg_bg_color = "lightgray"
        row.append(
            {
                "value": avg if avg is not None else "-",
                "class": "stats-centered",
                "color": avg_color,
                "bg_color": avg_bg_color,
            }
        )

        pace_table["rows"].append(
            {"row": row, "key": (-avg if avg is not None else math.inf, driver.name)}
        )

    pace_table["rows"].sort(key=lambda row: row["key"])
    ## Reset first val
    for i, row in enumerate(pace_table["rows"]):
        row["row"][0]["value"] = i + 1

    # Overtake table
    overtake_table = init_table(races=races, final_column="Total")

    for driver in drivers:
        row = []
        row.append({"value": 0, "class": "stats-padded"})
        row.append({"value": driver.name, "class": "stats-padded"})
        for entry in finish_dict[driver.id]:
            if entry is None or entry.overtakes is None:
                value = "-"
                color = None
                bg_color = "lightgray"
            else:
                value = entry.overtakes
                color, bg_color = overtake_colors(entry.overtakes)

            row.append(
                {
                    "value": value,
                    "class": "stats-centered",
                    "color": color,
                    "bg_color": bg_color,
                }
            )
        total = total_overtakes(finish_dict[driver.id])

        total_color, total_bg_color = total_overtake_colors(total)

        row.append(
            {
                "value": total,
                "class": "stats-centered",
                "color": total_color,
                "bg_color": total_bg_color,
                "key": total,
            }
        )

        overtake_table["rows"].append(
            {
                "row": row,
                "key": (-(total if total is not None else math.inf), driver.name),
            }
        )

    overtake_table["rows"].sort(key=lambda row: row["key"])
    ## Reset first val
    for i, row in enumerate(overtake_table["rows"]):
        row["row"][0]["value"] = i + 1

    # Best Results
    best_results_table = {
        "head": [
            {"value": "Driver"},
            {"value": "Race", "class": "stats-centered"},
            {"value": "Quali", "class": "stats-centered"},
        ],
        "rows": [],
    }

    for driver in drivers:
        row = []
        row.append({"value": driver.name, "class": "stats-padded"})

        if (
            best_race_result_dict[driver.id]
            and best_race_result_dict[driver.id].finish_position
        ):
            race_col, race_bg_col = finish_position_colors(
                best_race_result_dict[driver.id].finish_position
            )
            race_value = best_race_result_dict[driver.id].finish_position
            race_key = best_race_result_dict[driver.id].finish_position
        else:
            race_col, race_bg_col = (None, "lightgray")
            race_value = "-"
            race_key = math.inf

        if (
            best_quali_result_dict[driver.id]
            and best_quali_result_dict[driver.id].qualifying_position
        ):
            quali_col, quali_bg_col = finish_position_colors(
                best_quali_result_dict[driver.id].qualifying_position
            )
            quali_value = best_quali_result_dict[driver.id].qualifying_position
            quali_key = best_quali_result_dict[driver.id].qualifying_position
        else:
            quali_col, quali_bg_col = (None, "lightgray")
            quali_value = "-"
            quali_key = math.inf

        row.append(
            {
                "value": race_value,
                "class": "stats-centered",
                "color": race_col,
                "bg_color": race_bg_col,
            }
        )
        row.append(
            {
                "value": quali_value,
                "class": "stats-centered",
                "color": quali_col,
                "bg_color": quali_bg_col,
            }
        )

        best_results_table["rows"].append(
            {
                "row": row,
                "key": (race_key, quali_key, driver.name),
            }
        )

    best_results_table["rows"].sort(key=lambda row: row["key"])

    # Race Wins
    race_wins_table = {
        "head": [
            {"value": "Driver"},
            {"value": "Race", "class": "stats-centered"},
            {"value": "Quali", "class": "stats-centered"},
        ],
        "rows": [],
    }

    for driver in drivers:
        row = []
        row.append({"value": driver.name, "class": "stats-padded"})

        value = race_wins_dict[driver.id]

        row.append(
            {
                "value": value,
                "class": "stats-centered",
                "color": None,
                "bg_color": None,
            }
        )

        race_wins_table["rows"].append(
            {
                "row": row,
                "key": (-value, driver.name),
            }
        )

    race_wins_table["rows"].sort(key=lambda row: row["key"])

    tables = {
        "finish": race_classification_table,
        "quali": quali_classification_table,
        "pace": pace_table,
        "overtakes": overtake_table,
        "best_results": best_results_table,
    }

    stats_table = (
        races,
        {
            "best_results": sorted(
                [
                    (
                        driver,
                        best_race_result_dict[driver.id],
                        best_quali_result_dict[driver.id],
                    )
                    for driver in drivers
                ],
                key=lambda e: (
                    e[1].finish_position if e[1] else math.inf,
                    e[2].qualifying_position if e[2] else math.inf,
                ),
            ),
            "race_wins": {
                "entries": sorted(
                    [(driver, race_wins_dict[driver.id]) for driver in drivers],
                    key=lambda e: e[1],
                    reverse=True,
                ),
                "first": race_wins_unique[0] if len(race_wins_unique) > 0 else None,
                "second": race_wins_unique[1] if len(race_wins_unique) > 1 else None,
                "third": race_wins_unique[2] if len(race_wins_unique) > 2 else None,
            },
            "pace": sorted(
                [
                    {
                        "driver": driver,
                        "entries": pace_dict[driver.id],
                        "average": average_int(pace_dict[driver.id]),
                    }
                    for driver in drivers
                ],
                key=lambda e: e["average"] or -math.inf,
                reverse=True,
            ),
            "consecutive": sorted(
                [
                    {
                        "driver": driver,
                        "wins": {
                            "value": most_consecutive_wins[driver.id],
                            "first": most_consecutive_wins_unique[0]
                            if len(most_consecutive_wins_unique) > 0
                            else None,
                            "second": most_consecutive_wins_unique[1]
                            if len(most_consecutive_wins_unique) > 1
                            else None,
                            "third": most_consecutive_wins_unique[2]
                            if len(most_consecutive_wins_unique) > 2
                            else None,
                        },
                        "podiums": {
                            "value": most_consecutive_podiums[driver.id],
                            "first": most_consecutive_podiums_unique[0]
                            if len(most_consecutive_podiums_unique) > 0
                            else None,
                            "second": most_consecutive_podiums_unique[1]
                            if len(most_consecutive_podiums_unique) > 1
                            else None,
                            "third": most_consecutive_podiums_unique[2]
                            if len(most_consecutive_podiums_unique) > 2
                            else None,
                        },
                        "points": {
                            "value": most_consecutive_points[driver.id],
                            "first": most_consecutive_points_unique[0]
                            if len(most_consecutive_points_unique) > 0
                            else None,
                            "second": most_consecutive_points_unique[1]
                            if len(most_consecutive_points_unique) > 1
                            else None,
                            "third": most_consecutive_points_unique[2]
                            if len(most_consecutive_points_unique) > 2
                            else None,
                        },
                    }
                    for driver in drivers
                ],
                key=lambda e: (
                    e["wins"]["value"],
                    e["podiums"]["value"],
                    e["points"]["value"],
                ),
                reverse=True,
            ),
            "consecutive_without": sorted(
                [
                    {
                        "driver": driver,
                        "wins": {
                            "value": most_consecutive_no_wins[driver.id],
                            "first": most_consecutive_no_wins_unique[0]
                            if len(most_consecutive_no_wins_unique) > 0
                            else None,
                            "second": most_consecutive_no_wins_unique[1]
                            if len(most_consecutive_no_wins_unique) > 1
                            else None,
                            "third": most_consecutive_no_wins_unique[2]
                            if len(most_consecutive_no_wins_unique) > 2
                            else None,
                        },
                        "podiums": {
                            "value": most_consecutive_no_podiums[driver.id],
                            "first": most_consecutive_no_podiums_unique[0]
                            if len(most_consecutive_no_podiums_unique) > 0
                            else None,
                            "second": most_consecutive_no_podiums_unique[1]
                            if len(most_consecutive_no_podiums_unique) > 1
                            else None,
                            "third": most_consecutive_no_podiums_unique[2]
                            if len(most_consecutive_no_podiums_unique) > 2
                            else None,
                        },
                        "points": {
                            "value": most_consecutive_no_points[driver.id],
                            "first": most_consecutive_no_points_unique[0]
                            if len(most_consecutive_no_points_unique) > 0
                            else None,
                            "second": most_consecutive_no_points_unique[1]
                            if len(most_consecutive_no_points_unique) > 1
                            else None,
                            "third": most_consecutive_no_points_unique[2]
                            if len(most_consecutive_no_points_unique) > 2
                            else None,
                        },
                    }
                    for driver in drivers
                ],
                key=lambda e: (
                    e["podiums"]["value"],
                    e["points"]["value"],
                    e["wins"]["value"],
                ),
                reverse=True,
            ),
            "before_first_win": sorted(
                [
                    {
                        "driver": driver,
                        "races": {
                            "value": most_consecutive_first_races[driver.id],
                            "first": most_consecutive_first_races_unique[0]
                            if len(most_consecutive_first_races_unique) > 0
                            else None,
                            "second": most_consecutive_first_races_unique[1]
                            if len(most_consecutive_first_races_unique) > 1
                            else None,
                            "third": most_consecutive_first_races_unique[2]
                            if len(most_consecutive_first_races_unique) > 2
                            else None,
                        },
                        "podiums": {
                            "value": most_consecutive_first_podiums[driver.id],
                            "first": most_consecutive_first_podiums_unique[0]
                            if len(most_consecutive_first_podiums_unique) > 0
                            else None,
                            "second": most_consecutive_first_podiums_unique[1]
                            if len(most_consecutive_first_podiums_unique) > 1
                            else None,
                            "third": most_consecutive_first_podiums_unique[2]
                            if len(most_consecutive_first_podiums_unique) > 2
                            else None,
                        },
                        "points": {
                            "value": most_consecutive_first_points[driver.id],
                            "first": most_consecutive_first_points_unique[0]
                            if len(most_consecutive_first_points_unique) > 0
                            else None,
                            "second": most_consecutive_first_points_unique[1]
                            if len(most_consecutive_first_points_unique) > 1
                            else None,
                            "third": most_consecutive_first_points_unique[2]
                            if len(most_consecutive_first_points_unique) > 2
                            else None,
                        },
                    }
                    for driver in drivers
                ],
                key=lambda e: (
                    e["podiums"]["value"],
                    e["points"]["value"],
                    e["races"]["value"],
                ),
                reverse=True,
            ),
        },
    )
    return (stats_table, tables)
