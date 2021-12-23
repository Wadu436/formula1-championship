import datetime
import os

import django
import django.utils.timezone as tz
import pytz
from django.core.files import File
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
        full_laps=63,
        long_laps=31,
        medium_laps=16,
    )
    with open("track_images/Schedule Austria.png", "rb") as file:
        track.overview_image.save("Schedule_Austria.png", File(file))
        track.save()
    with open("track_images/Layout Austria.png", "rb") as file:
        track.detail_image.save("Layout_Austria.png", File(file))
        track.save()

    track2: Track = Track.objects.create(
        location="Italy",
        name="Monza Circuit",
        abbreviation="ITA",
        country="it",
        full_laps=56,
        long_laps=28,
        medium_laps=14,
    )
    with open("track_images/Schedule Monza.png", "rb") as file:
        track2.overview_image.save("Schedule_Monza.png", File(file))
        track2.save()

    track3: Track = Track.objects.create(
        location="Netherlands",
        name="Circuit Zandvoort",
        abbreviation="NED",
        country="nl",
        full_laps=66,
        long_laps=33,
        medium_laps=17,
    )
    with open("track_images/Schedule Netherlands.png", "rb") as file:
        track3.overview_image.save("Schedule_Netherlands.png", File(file))
        track3.save()

    track4: Track = Track.objects.create(
        location="Mexico",
        name="Autódromo Hermanos Rodríguez",
        abbreviation="MXC",
        country="mx",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Mexico.png", "rb") as file:
        track4.overview_image.save("Schedule_Mexico.png", File(file))
        track4.save()

    track5: Track = Track.objects.create(
        location="Monaco",
        name="Circuit de Monaco",
        abbreviation="MON",
        country="mc",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Monaco.png", "rb") as file:
        track5.overview_image.save("Schedule_Monaco.png", File(file))
        track5.save()

    track6: Track = Track.objects.create(
        location="Brazil",
        name="Interlagos Circuit",
        abbreviation="SAP",
        country="br",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Brazil.png", "rb") as file:
        track6.overview_image.save("Schedule_Brazil.png", File(file))
        track6.save()

    track7: Track = Track.objects.create(
        location="Australia",
        name="Albert Park Circuit",
        abbreviation="AUS",
        country="au",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Australia.png", "rb") as file:
        track7.overview_image.save("Schedule_Australia.png", File(file))
        track7.save()

    track8: Track = Track.objects.create(
        location="Spain",
        name="Circuit de Barcelona-Catalunya",
        abbreviation="SPA",
        country="es",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Spain.png", "rb") as file:
        track8.overview_image.save("Schedule_Spain.png", File(file))
        track8.save()

    track9: Track = Track.objects.create(
        location="Japan",
        name="Suzuka International Racing Course",
        abbreviation="JPN",
        country="jp",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Japan.png", "rb") as file:
        track9.overview_image.save("Schedule_Japan.png", File(file))
        track9.save()

    track10: Track = Track.objects.create(
        location="France",
        name="Circuit Paul Ricard",
        abbreviation="FRA",
        country="fr",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule France.png", "rb") as file:
        track10.overview_image.save("Schedule_France.png", File(file))
        track10.save()

    track11: Track = Track.objects.create(
        location="Portugal",
        name="Algarve International Circuit",
        abbreviation="POR",
        country="pt",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Portugal.png", "rb") as file:
        track11.overview_image.save("Schedule_Portugal.png", File(file))
        track11.save()

    track12: Track = Track.objects.create(
        location="Singapore",
        name="Marina Bay Street Circuit",
        abbreviation="SIN",
        country="sg",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Singapore.png", "rb") as file:
        track12.overview_image.save("Schedule_Singapore.png", File(file))
        track12.save()

    track13: Track = Track.objects.create(
        location="Italy",
        name="Imola Circuit",
        abbreviation="EMI",
        country="it",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Imola.png", "rb") as file:
        track13.overview_image.save("Schedule_Imola.png", File(file))
        track13.save()

    track14: Track = Track.objects.create(
        location="Belgium",
        name="Circuit de Spa-Francorchamps",
        abbreviation="BEL",
        country="be",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Belgium.png", "rb") as file:
        track14.overview_image.save("Schedule_Belgium.png", File(file))
        track14.save()

    track15: Track = Track.objects.create(
        location="Bahrain",
        name="Bahrain International Circuit",
        abbreviation="BHR",
        country="bh",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Bahrain.png", "rb") as file:
        track15.overview_image.save("Schedule_Bahrain.png", File(file))
        track15.save()

    track16: Track = Track.objects.create(
        location="Great Britain",
        name="Silverstone Circuit",
        abbreviation="GBR",
        country="gb",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Great Britain.png", "rb") as file:
        track16.overview_image.save("Schedule_Great_Britain.png", File(file))
        track16.save()

    track17: Track = Track.objects.create(
        location="Azerbaijan",
        name="Baku City Circuit",
        abbreviation="AZE",
        country="az",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Azerbaijan.png", "rb") as file:
        track17.overview_image.save("Schedule_Azerbaijan.png", File(file))
        track17.save()

    track18: Track = Track.objects.create(
        location="China",
        name="Shanghai International Circuit",
        abbreviation="CHN",
        country="cn",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule China.png", "rb") as file:
        track18.overview_image.save("Schedule_China.png", File(file))
        track18.save()

    track19: Track = Track.objects.create(
        location="Hungary",
        name="Hungaroring",
        abbreviation="HUN",
        country="hu",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Hungary.png", "rb") as file:
        track19.overview_image.save("Schedule_Hungary.png", File(file))
        track19.save()

    track20: Track = Track.objects.create(
        location="United States",
        name="Circuit of the Americas",
        abbreviation="USA",
        country="us",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule USA.png", "rb") as file:
        track20.overview_image.save("Schedule_USA.png", File(file))
        track20.save()

    track21: Track = Track.objects.create(
        location="Canada",
        name="Circuit Gilles Villeneuve",
        abbreviation="CAN",
        country="ca",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Canada.png", "rb") as file:
        track21.overview_image.save("Schedule_Canada.png", File(file))
        track21.save()

    track22: Track = Track.objects.create(
        location="Russia",
        name="Sochi Autodrom",
        abbreviation="RUS",
        country="ru",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Russia.png", "rb") as file:
        track22.overview_image.save("Schedule_Russia.png", File(file))
        track22.save()

    track23: Track = Track.objects.create(
        location="Saudi Arabia",
        name="Jeddah Corniche Circuit",
        abbreviation="SAU",
        country="sa",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Saudi Arabia.png", "rb") as file:
        track23.overview_image.save("Schedule_Saudi_Arabia.png", File(file))
        track23.save()

    track24: Track = Track.objects.create(
        location="Abu Dhabi",
        name="Yas Marina Circuit",
        abbreviation="ARE",
        country="ae",
        full_laps=60,
        long_laps=30,
        medium_laps=15,
    )
    with open("track_images/Schedule Abu Dhabi.png", "rb") as file:
        track24.overview_image.save("Schedule_Abu_Dhabi.png", File(file))
        track24.save()

    red_bull: Team = Team.objects.create(
        name="Red Bull",
        full_name="Red Bull Racing Honda",
        color="#0600ef",
        country="at",
    )
    ferrari: Team = Team.objects.create(
        name="Ferrari",
        full_name="Scuderia Ferrari Mission Winnow",
        color="#dc0000",
        country="it",
    )
    mclaren: Team = Team.objects.create(
        name="McLaren",
        full_name="McLaren F1 Team",
        color="#FF9800",
        country="gb",
    )
    alphatauri: Team = Team.objects.create(
        name="AlphaTauri",
        full_name="Scuderia AlphaTauri Honda",
        color="#2b4562",
        country="it",
    )
    aston_martin: Team = Team.objects.create(
        name="Aston Martin",
        full_name="Aston Martin Cognizant F1 Team",
        color="#006f62",
        country="gb",
    )
    williams: Team = Team.objects.create(
        name="Williams",
        full_name="Williams Racing",
        color="#005aff",
        country="gb",
    )
    alfa_romeo: Team = Team.objects.create(
        name="Alfa Romeo Racing",
        full_name="Alfa Romeo Racing ORLEN",
        color="#900000",
        country="ch",
    )
    haas: Team = Team.objects.create(
        name="Haas", full_name="Uralkali Haas F1 Team", color="#ffffff", country="us"
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

    championship: Championship = Championship.objects.create(
        name="NAMR1 F1 Season One Championship",
        start_date=datetime.date(year=2021, month=10, day=24),
    )

    TIMEZONE = pytz.timezone("Europe/Brussels")

    race: Race = Race.objects.create(
        championship_order=1,
        championship=championship,
        track=track,
        date_time=TIMEZONE.localize(datetime.datetime(2021, 10, 24, 15, 30)),
        finished=True,
        length="M",
    )

    race2: Race = Race.objects.create(
        championship_order=2,
        championship=championship,
        track=track2,
        date_time=TIMEZONE.localize(datetime.datetime(2021, 10, 24, 17, 15)),
        finished=True,
        length="M",
    )

    race3: Race = Race.objects.create(
        championship_order=3,
        championship=championship,
        track=track3,
        date_time=TIMEZONE.localize(datetime.datetime(2021, 10, 29, 22, 00)),
        length="M",
    )
    race4: Race = Race.objects.create(
        championship_order=4,
        championship=championship,
        track=track4,
        date_time=None,
        length="M",
    )

    ## Race 1
    # Finished entries
    race.race_entries.create(
        driver=warre,
        team=warre.team,
        qualifying_position=1,
        finish_position=1,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=731),
        tires="SM",
    )
    race.race_entries.create(
        driver=martijn_vd,
        team=martijn_vd.team,
        qualifying_position=14,
        finish_position=2,
        best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=286),
        tires="SM",
    )
    race.race_entries.create(
        driver=nam,
        team=nam.team,
        qualifying_position=4,
        finish_position=3,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
        tires="MS",
    )
    race.race_entries.create(
        bot=True,
        finish_position=4,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
        tires="MS",
    )
    race.race_entries.create(
        driver=charles,
        team=charles.team,
        qualifying_position=2,
        finish_position=5,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=519),
        tires="MS",
    )
    race.race_entries.create(
        driver=kevin,
        team=kevin.team,
        qualifying_position=7,
        finish_position=6,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=772),
        tires="SM",
    )
    race.race_entries.create(
        driver=david,
        team=david.team,
        qualifying_position=5,
        finish_position=7,
        best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=724),
        tires="SM",
    )
    race.race_entries.create(
        driver=tim,
        team=tim.team,
        qualifying_position=3,
        finish_position=8,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=402),
        tires="SM",
    )
    race.race_entries.create(
        bot=True,
        finish_position=9,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
        tires="SM",
    )
    race.race_entries.create(
        bot=True,
        finish_position=10,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
        tires="SM",
    )
    race.race_entries.create(
        driver=brandon,
        team=brandon.team,
        qualifying_position=13,
        finish_position=11,
        best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=298),
        tires="MH",
    )
    race.race_entries.create(
        driver=jorrick,
        team=jorrick.team,
        qualifying_position=6,
        finish_position=12,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=750),
        tires="SM",
    )
    race.race_entries.create(
        driver=arda,
        team=arda.team,
        qualifying_position=10,
        finish_position=13,
        best_lap_time=datetime.timedelta(minutes=1, seconds=9, milliseconds=721),
        tires="SH",
    )
    race.race_entries.create(
        driver=jeroen,
        team=jeroen.team,
        qualifying_position=8,
        finish_position=14,
        best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=962),
        tires="SM",
    )
    race.race_entries.create(
        driver=albion,
        team=albion.team,
        qualifying_position=11,
        finish_position=15,
        best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=545),
        tires="SMHMIHSMHWHMSMHIWHSMHMSM",
    )

    # DNA entries
    race.dna_entries.create(
        driver=frank,
        team=frank.team,
    )
    race.dna_entries.create(
        driver=martijn_p,
        team=martijn_p.team,
    )
    race.dna_entries.create(
        driver=bryan,
        team=bryan.team,
    )

    ## Race 2
    race2.race_entries.create(
        driver=jorrick,
        team=jorrick.team,
        qualifying_position=1,
        finish_position=1,
        best_lap_time=datetime.timedelta(minutes=1, seconds=23, milliseconds=499),
    )

    race2.race_entries.create(
        driver=brandon,
        team=brandon.team,
        qualifying_position=4,
        finish_position=2,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=466),
    )
    race2.race_entries.create(
        bot=True,
        finish_position=3,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )
    race2.race_entries.create(
        driver=kevin,
        team=kevin.team,
        qualifying_position=10,
        finish_position=4,
        best_lap_time=datetime.timedelta(minutes=1, seconds=24, milliseconds=341),
    )

    race2.race_entries.create(
        driver=jeroen,
        team=jeroen.team,
        qualifying_position=7,
        finish_position=5,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=433),
    )

    race2.race_entries.create(
        driver=nam,
        team=nam.team,
        qualifying_position=6,
        finish_position=6,
        best_lap_time=datetime.timedelta(minutes=1, seconds=23, milliseconds=977),
    )

    race2.race_entries.create(
        driver=charles,
        team=charles.team,
        qualifying_position=3,
        finish_position=7,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=581),
    )
    race2.race_entries.create(
        bot=True,
        finish_position=8,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )
    race2.race_entries.create(
        bot=True,
        finish_position=9,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )
    race2.race_entries.create(
        bot=True,
        finish_position=10,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )
    race2.race_entries.create(
        driver=arda,
        team=arda.team,
        qualifying_position=8,
        finish_position=11,
        best_lap_time=datetime.timedelta(minutes=1, seconds=26, milliseconds=88),
    )

    race2.race_entries.create(
        driver=albion,
        team=albion.team,
        qualifying_position=15,
        finish_position=12,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=138),
    )

    race2.race_entries.create(
        driver=david,
        team=david.team,
        dnf=True,
        qualifying_position=2,
        finish_position=13,
        best_lap_time=datetime.timedelta(minutes=1, seconds=24, milliseconds=149),
    )

    race2.race_entries.create(
        driver=warre,
        team=warre.team,
        dnf=True,
        qualifying_position=5,
        finish_position=14,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=803),
    )
    race2.race_entries.create(
        bot=True,
        finish_position=15,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )

    # DNA's
    race2.dna_entries.create(
        driver=frank,
        team=frank.team,
    )

    race2.dna_entries.create(
        driver=martijn_p,
        team=martijn_p.team,
    )
    race2.dna_entries.create(
        driver=martijn_vd,
        team=martijn_vd.team,
    )
    race2.dna_entries.create(
        driver=bryan,
        team=bryan.team,
    )
    race2.dna_entries.create(
        driver=tim,
        team=tim.team,
    )

    # Add it again :)

    championship: Championship = Championship.objects.create(
        name="NAMR1 F1 Season Two Championship",
        start_date=datetime.date(year=2022, month=2, day=10),
    )

    race: Race = Race.objects.create(
        championship_order=1,
        championship=championship,
        track=track,
        date_time=now(),
        length="M",
        finished=True,
    )

    race2: Race = Race.objects.create(
        championship_order=2,
        championship=championship,
        track=track2,
        date_time=now(),
        length="M",
        finished=True,
    )

    ## Race 1
    # Finished entries
    race.race_entries.create(
        driver=warre,
        team=warre.team,
        qualifying_position=1,
        finish_position=1,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=731),
    )
    race.race_entries.create(
        driver=martijn_vd,
        team=martijn_vd.team,
        qualifying_position=14,
        finish_position=2,
        best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=286),
    )
    race.race_entries.create(
        driver=nam,
        team=nam.team,
        qualifying_position=4,
        finish_position=3,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )
    race.race_entries.create(
        bot=True,
        finish_position=4,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )
    race.race_entries.create(
        driver=charles,
        team=charles.team,
        qualifying_position=2,
        finish_position=5,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=519),
    )
    race.race_entries.create(
        driver=kevin,
        team=kevin.team,
        qualifying_position=7,
        finish_position=6,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=772),
    )
    race.race_entries.create(
        driver=david,
        team=david.team,
        qualifying_position=5,
        finish_position=7,
        best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=724),
    )
    race.race_entries.create(
        driver=tim,
        team=tim.team,
        qualifying_position=3,
        finish_position=8,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=402),
    )
    race.race_entries.create(
        bot=True,
        finish_position=9,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )
    race.race_entries.create(
        bot=True,
        finish_position=10,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
    )
    race.race_entries.create(
        driver=brandon,
        team=brandon.team,
        qualifying_position=13,
        finish_position=11,
        best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=298),
    )
    race.race_entries.create(
        driver=jorrick,
        team=jorrick.team,
        qualifying_position=6,
        finish_position=12,
        best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=750),
    )
    race.race_entries.create(
        driver=arda,
        team=arda.team,
        qualifying_position=10,
        finish_position=13,
        best_lap_time=datetime.timedelta(minutes=1, seconds=9, milliseconds=721),
    )
    race.race_entries.create(
        driver=jeroen,
        team=jeroen.team,
        qualifying_position=8,
        finish_position=14,
        best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=962),
    )
    race.race_entries.create(
        driver=albion,
        team=albion.team,
        qualifying_position=11,
        finish_position=15,
        best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=545),
    )

    # DNA entries
    race.dna_entries.create(
        driver=frank,
        team=frank.team,
    )
    race.dna_entries.create(
        driver=martijn_p,
        team=martijn_p.team,
    )
    race.dna_entries.create(
        driver=bryan,
        team=bryan.team,
    )

    ## Race 2
    race2.race_entries.create(
        driver=david,
        team=david.team,
        dnf=True,
        qualifying_position=2,
        finish_position=1,
        best_lap_time=datetime.timedelta(minutes=1, seconds=24, milliseconds=149),
    )
    race2.race_entries.create(
        driver=warre,
        team=warre.team,
        dnf=True,
        qualifying_position=5,
        finish_position=2,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=803),
    )
    race2.race_entries.create(
        driver=jorrick,
        team=jorrick.team,
        qualifying_position=1,
        finish_position=3,
        best_lap_time=datetime.timedelta(minutes=1, seconds=23, milliseconds=499),
    )
    race2.race_entries.create(
        driver=kevin,
        team=kevin.team,
        qualifying_position=10,
        finish_position=4,
        best_lap_time=datetime.timedelta(minutes=1, seconds=24, milliseconds=341),
    )

    race2.race_entries.create(
        driver=jeroen,
        team=jeroen.team,
        qualifying_position=7,
        finish_position=5,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=433),
    )

    race2.race_entries.create(
        driver=charles,
        team=charles.team,
        qualifying_position=3,
        finish_position=6,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=581),
    )

    race2.race_entries.create(
        driver=nam,
        team=nam.team,
        qualifying_position=6,
        finish_position=7,
        best_lap_time=datetime.timedelta(minutes=1, seconds=23, milliseconds=977),
    )

    race2.race_entries.create(
        bot=True,
        finish_position=8,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=500),
    )

    race2.race_entries.create(
        bot=True,
        finish_position=9,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=500),
    )

    race2.race_entries.create(
        bot=True,
        finish_position=10,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=500),
    )

    race2.race_entries.create(
        driver=arda,
        team=arda.team,
        qualifying_position=8,
        finish_position=11,
        best_lap_time=datetime.timedelta(minutes=1, seconds=26, milliseconds=88),
    )

    race2.race_entries.create(
        driver=albion,
        team=albion.team,
        qualifying_position=15,
        finish_position=12,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=138),
    )
    race2.race_entries.create(
        bot=True,
        finish_position=13,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=500),
    )

    race2.race_entries.create(
        driver=brandon,
        team=brandon.team,
        qualifying_position=4,
        finish_position=14,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=466),
    )

    race2.race_entries.create(
        bot=True,
        finish_position=15,
        best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=500),
    )



    # DNA's
    race2.dna_entries.create(
        driver=frank,
        team=frank.team,
    )

    race2.dna_entries.create(
        driver=martijn_p,
        team=martijn_p.team,
    )
    race2.dna_entries.create(
        driver=martijn_vd,
        team=martijn_vd.team,
    )
    race2.dna_entries.create(
        driver=bryan,
        team=bryan.team,
    )
    race2.dna_entries.create(
        driver=tim,
        team=tim.team,
    )
