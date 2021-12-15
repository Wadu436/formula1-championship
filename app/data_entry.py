import datetime
import os

import django
from django.utils.timezone import now

# Configure Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from leaderboard.models import (Championship, Driver, Race, RaceEntry, Team,
                                Track)

ADD_DATA = True

# Delete All
RaceEntry.objects.all().delete()
Race.objects.all().delete()
Driver.objects.all().delete()
Championship.objects.all().delete()
Team.objects.all().delete()
Track.objects.all().delete()

if ADD_DATA:
    track: Track = Track.objects.create(
        location="Austria",
        name="Red Bull Ring",
        abbreviation="AUT",
        country="at",
    )

    track2: Track = Track.objects.create(
        location="Italy",
        name="Monza",
        abbreviation="ITA",
        country="it",
    )

    ferrari: Team = Team.objects.create(
        name="Scuderia Ferrari", color="#D40000", country="it"
    )
    red_bull: Team = Team.objects.create(
        name="Red Bull Racing",
        color="#1D19AC",
        country="at",
    )
    alphatauri: Team = Team.objects.create(
        name="AlphaTauri",
        color="#03BFB5",
        country="de",
    )
    haas: Team = Team.objects.create(name="Haas", color="#D40000", country="it")
    mclaren: Team = Team.objects.create(
        name="McLaren",
        color="#1D19AC",
        country="at",
    )
    williams: Team = Team.objects.create(
        name="Williams",
        color="#03BFB5",
        country="de",
    )
    alfa_romeo: Team = Team.objects.create(
        name="Alfa Romeo",
        color="#1D19AC",
        country="at",
    )
    aston_martin: Team = Team.objects.create(
        name="Aston Martin",
        color="#03BFB5",
        country="de",
    )

    championship: Championship = Championship.objects.create(
        name="NAMR1 F1 Season One Championship", start_date=datetime.date(year=2021, month=10, day=24)
    )

    nam: Driver = Driver.objects.create(name="Nam", team=ferrari, country="nl")
    warre: Driver = Driver.objects.create(name="Warre", team=alfa_romeo, country="be")
    david: Driver = Driver.objects.create(name="David", team=mclaren, country="nl")
    charles: Driver = Driver.objects.create(name="Charles", team=red_bull, country="nl")
    jorrick: Driver = Driver.objects.create(
        name="Jorrick", team=aston_martin, country="nl"
    )
    frank: Driver = Driver.objects.create(name="Frank", team=red_bull, country="nl")
    arda: Driver = Driver.objects.create(name="Arda", team=aston_martin, country="nl")
    martijn_p: Driver = Driver.objects.create(
        name="Martijn P.", team=williams, country="nl"
    )
    jeroen: Driver = Driver.objects.create(name="Jeroen", team=ferrari, country="nl")
    albion: Driver = Driver.objects.create(name="Albion", team=williams, country="nl")
    tim: Driver = Driver.objects.create(name="Tim", team=haas, country="nl")
    bryan: Driver = Driver.objects.create(name="Bryan", team=haas, country="nl")
    martijn_vd: Driver = Driver.objects.create(
        name="Martijn v. D.", team=alfa_romeo, country="nl"
    )
    brandon: Driver = Driver.objects.create(
        name="Brandon", team=alphatauri, country="nl"
    )
    kevin: Driver = Driver.objects.create(name="Kevin", team=alphatauri, country="nl")

    race: Race = Race.objects.create(
        championship_order=1,
        championship=championship,
        track=track,
        date_time=now(),
    )

    race2: Race = Race.objects.create(
        championship_order=2,
        championship=championship,
        track=track2,
        date_time=now(),
    )

    ## Race 1
    # Finished entries
    race.race_entries.create(
        driver=warre,
        team=warre.team,
        dna=False,
        qualifying_position=1,
        finish_position=1,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=731),
    )
    race.race_entries.create(
        driver=martijn_vd,
        team=martijn_vd.team,
        dna=False,
        qualifying_position=14,
        finish_position=2,
        best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=286),
    )
    race.race_entries.create(
        driver=nam,
        team=nam.team,
        dna=False,
        qualifying_position=4,
        finish_position=3,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )
    race.race_entries.create(
        driver=charles,
        team=charles.team,
        dna=False,
        qualifying_position=2,
        finish_position=5,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=519),
    )
    race.race_entries.create(
        driver=kevin,
        team=kevin.team,
        dna=False,
        qualifying_position=7,
        finish_position=6,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=772),
    )
    race.race_entries.create(
        driver=david,
        team=david.team,
        dna=False,
        qualifying_position=5,
        finish_position=7,
        best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=724),
    )
    race.race_entries.create(
        driver=tim,
        team=tim.team,
        dna=False,
        qualifying_position=3,
        finish_position=8,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=402),
    )
    race.race_entries.create(
        driver=brandon,
        team=brandon.team,
        dna=False,
        qualifying_position=13,
        finish_position=11,
        best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=298),
    )
    race.race_entries.create(
        driver=jorrick,
        team=jorrick.team,
        dna=False,
        qualifying_position=6,
        finish_position=12,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=750),
    )
    race.race_entries.create(
        driver=arda,
        team=arda.team,
        dna=False,
        qualifying_position=10,
        finish_position=12,
        best_lap_time=datetime.timedelta(minutes=1, seconds=9, milliseconds=721),
    )
    race.race_entries.create(
        driver=jeroen,
        team=jeroen.team,
        dna=False,
        qualifying_position=8,
        finish_position=14,
        best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=962),
    )
    race.race_entries.create(
        driver=albion,
        team=albion.team,
        dna=False,
        qualifying_position=11,
        finish_position=15,
        best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=545),
    )

    # DNA entries
    race.race_entries.create(
        driver=frank,
        team=frank.team,
        dna=True,
    )
    race.race_entries.create(
        driver=martijn_p,
        team=martijn_p.team,
        dna=True,
    )
    race.race_entries.create(
        driver=bryan,
        team=bryan.team,
        dna=True,
    )

    ## Race 2
    race2.race_entries.create(
        driver=jorrick,
        team=jorrick.team,
        dna=False,
        qualifying_position=1,
        finish_position=1,
        best_lap_time=datetime.timedelta(minutes=1, seconds=23, milliseconds=499),
    )

    race2.race_entries.create(
        driver=brandon,
        team=brandon.team,
        dna=False,
        qualifying_position=4,
        finish_position=2,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=466),
    )

    race2.race_entries.create(
        driver=kevin,
        team=kevin.team,
        dna=False,
        qualifying_position=10,
        finish_position=4,
        best_lap_time=datetime.timedelta(minutes=1, seconds=24, milliseconds=341),
    )

    race2.race_entries.create(
        driver=jeroen,
        team=jeroen.team,
        dna=False,
        qualifying_position=7,
        finish_position=5,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=433),
    )

    race2.race_entries.create(
        driver=nam,
        team=nam.team,
        dna=False,
        qualifying_position=6,
        finish_position=6,
        best_lap_time=datetime.timedelta(minutes=1, seconds=23, milliseconds=977),
    )

    race2.race_entries.create(
        driver=charles,
        team=charles.team,
        dna=False,
        qualifying_position=3,
        finish_position=7,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=581),
    )

    race2.race_entries.create(
        driver=arda,
        team=arda.team,
        dna=False,
        qualifying_position=8,
        finish_position=11,
        best_lap_time=datetime.timedelta(minutes=1, seconds=26, milliseconds=88),
    )

    race2.race_entries.create(
        driver=albion,
        team=albion.team,
        dna=False,
        qualifying_position=15,
        finish_position=12,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=138),
    )

    race2.race_entries.create(
        driver=david,
        team=david.team,
        dna=False,
        dnf=True,
        qualifying_position=2,
        finish_position=13,
        best_lap_time=datetime.timedelta(minutes=1, seconds=24, milliseconds=149),
    )

    race2.race_entries.create(
        driver=warre,
        team=warre.team,
        dna=False,
        dnf=True,
        qualifying_position=5,
        finish_position=14,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=803),
    )

    # DNA's
    race2.race_entries.create(
        driver=frank,
        team=frank.team,
        dna=True,
    )

    race2.race_entries.create(
        driver=martijn_p,
        team=martijn_p.team,
        dna=True,
    )
    race2.race_entries.create(
        driver=martijn_vd,
        team=martijn_vd.team,
        dna=True,
    )
    race2.race_entries.create(
        driver=bryan,
        team=bryan.team,
        dna=True,
    )
    race2.race_entries.create(
        driver=tim,
        team=tim.team,
        dna=True,
    )