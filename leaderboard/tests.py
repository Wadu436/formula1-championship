import datetime

from django.test import TestCase
from django.utils.timezone import now

from .models import Championship, Driver, Race, RaceEntry, Team, Track


# Create your tests here.
class ChampionshipTest(TestCase):
    def setUp(self):
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

        self.championship: Championship = Championship.objects.create(
            name="NAMR1 F1 Season One Championship"
        )

        self.nam: Driver = Driver.objects.create(name="Nam", team=ferrari, country="nl")
        self.warre: Driver = Driver.objects.create(
            name="Warre", team=alfa_romeo, country="be"
        )
        self.david: Driver = Driver.objects.create(
            name="David", team=mclaren, country="nl"
        )
        self.charles: Driver = Driver.objects.create(
            name="Charles", team=red_bull, country="nl"
        )
        self.jorrick: Driver = Driver.objects.create(
            name="Jorrick", team=aston_martin, country="nl"
        )
        self.frank: Driver = Driver.objects.create(
            name="Frank", team=red_bull, country="nl"
        )
        self.arda: Driver = Driver.objects.create(
            name="Arda", team=aston_martin, country="nl"
        )
        self.martijn_p: Driver = Driver.objects.create(
            name="Martijn P.", team=williams, country="nl"
        )
        self.jeroen: Driver = Driver.objects.create(
            name="Jeroen", team=ferrari, country="nl"
        )
        self.albion: Driver = Driver.objects.create(
            name="Albion", team=williams, country="nl"
        )
        self.tim: Driver = Driver.objects.create(name="Tim", team=haas, country="nl")
        self.bryan: Driver = Driver.objects.create(
            name="Bryan", team=haas, country="nl"
        )
        self.martijn_vd: Driver = Driver.objects.create(
            name="Martijn v. D.", team=alfa_romeo, country="nl"
        )
        self.brandon: Driver = Driver.objects.create(
            name="Brandon", team=alphatauri, country="nl"
        )
        self.kevin: Driver = Driver.objects.create(
            name="Kevin", team=alphatauri, country="nl"
        )

        self.race: Race = Race.objects.create(
            championship_order=1,
            championship=self.championship,
            track=track,
            date_time=now(),
        )

        self.race2: Race = Race.objects.create(
            championship_order=2,
            championship=self.championship,
            track=track2,
            date_time=now(),
        )

        ## Race 1
        # Finished entries
        self.race.race_entries.create(
            driver=self.warre,
            team=self.warre.team,
            dna=False,
            qualifying_position=1,
            finish_position=1,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=731),
        )
        self.race.race_entries.create(
            driver=self.martijn_vd,
            team=self.martijn_vd.team,
            dna=False,
            qualifying_position=14,
            finish_position=2,
            best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=286),
        )
        self.race.race_entries.create(
            driver=self.nam,
            team=self.nam.team,
            dna=False,
            qualifying_position=4,
            finish_position=3,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
        )
        self.race.race_entries.create(
            driver=self.charles,
            team=self.charles.team,
            dna=False,
            qualifying_position=2,
            finish_position=5,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=519),
        )
        self.race.race_entries.create(
            driver=self.kevin,
            team=self.kevin.team,
            dna=False,
            qualifying_position=7,
            finish_position=6,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=772),
        )
        self.race.race_entries.create(
            driver=self.david,
            team=self.david.team,
            dna=False,
            qualifying_position=5,
            finish_position=7,
            best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=724),
        )
        self.race.race_entries.create(
            driver=self.tim,
            team=self.tim.team,
            dna=False,
            qualifying_position=3,
            finish_position=8,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=402),
        )
        self.race.race_entries.create(
            driver=self.brandon,
            team=self.brandon.team,
            dna=False,
            qualifying_position=13,
            finish_position=11,
            best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=298),
        )
        self.race.race_entries.create(
            driver=self.jorrick,
            team=self.jorrick.team,
            dna=False,
            qualifying_position=6,
            finish_position=12,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=750),
        )
        self.race.race_entries.create(
            driver=self.arda,
            team=self.arda.team,
            dna=False,
            qualifying_position=10,
            finish_position=12,
            best_lap_time=datetime.timedelta(minutes=1, seconds=9, milliseconds=721),
        )
        self.race.race_entries.create(
            driver=self.jeroen,
            team=self.jeroen.team,
            dna=False,
            qualifying_position=8,
            finish_position=14,
            best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=962),
        )
        self.race.race_entries.create(
            driver=self.albion,
            team=self.albion.team,
            dna=False,
            qualifying_position=11,
            finish_position=15,
            best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=545),
        )

        # DNA entries
        self.race.race_entries.create(
            driver=self.frank,
            team=self.frank.team,
            dna=True,
        )
        self.race.race_entries.create(
            driver=self.martijn_p,
            team=self.martijn_p.team,
            dna=True,
        )
        self.race.race_entries.create(
            driver=self.bryan,
            team=self.bryan.team,
            dna=True,
        )

        ## Race 2
        self.race2.race_entries.create(
            driver=self.jorrick,
            team=self.jorrick.team,
            dna=False,
            qualifying_position=1,
            finish_position=1,
            best_lap_time=datetime.timedelta(minutes=1, seconds=23, milliseconds=499),
        )

        self.race2.race_entries.create(
            driver=self.brandon,
            team=self.brandon.team,
            dna=False,
            qualifying_position=4,
            finish_position=2,
            best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=466),
        )

        self.race2.race_entries.create(
            driver=self.kevin,
            team=self.kevin.team,
            dna=False,
            qualifying_position=10,
            finish_position=4,
            best_lap_time=datetime.timedelta(minutes=1, seconds=24, milliseconds=341),
        )

        self.race2.race_entries.create(
            driver=self.jeroen,
            team=self.jeroen.team,
            dna=False,
            qualifying_position=7,
            finish_position=5,
            best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=433),
        )

        self.race2.race_entries.create(
            driver=self.nam,
            team=self.nam.team,
            dna=False,
            qualifying_position=6,
            finish_position=6,
            best_lap_time=datetime.timedelta(minutes=1, seconds=23, milliseconds=977),
        )

        self.race2.race_entries.create(
            driver=self.charles,
            team=self.charles.team,
            dna=False,
            qualifying_position=3,
            finish_position=7,
            best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=581),
        )

        self.race2.race_entries.create(
            driver=self.arda,
            team=self.arda.team,
            dna=False,
            qualifying_position=8,
            finish_position=11,
            best_lap_time=datetime.timedelta(minutes=1, seconds=26, milliseconds=88),
        )

        self.race2.race_entries.create(
            driver=self.albion,
            team=self.albion.team,
            dna=False,
            qualifying_position=15,
            finish_position=12,
            best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=138),
        )

        self.race2.race_entries.create(
            driver=self.david,
            team=self.david.team,
            dna=False,
            dnf=True,
            qualifying_position=2,
            finish_position=13,
            best_lap_time=datetime.timedelta(minutes=1, seconds=24, milliseconds=149),
        )

        self.race2.race_entries.create(
            driver=self.warre,
            team=self.warre.team,
            dna=False,
            dnf=True,
            qualifying_position=5,
            finish_position=14,
            best_lap_time=datetime.timedelta(minutes=1, seconds=25, milliseconds=803),
        )

        # DNA's
        self.race2.race_entries.create(
            driver=self.frank,
            team=self.frank.team,
            dna=True,
        )

        self.race2.race_entries.create(
            driver=self.martijn_p,
            team=self.martijn_p.team,
            dna=True,
        )
        self.race2.race_entries.create(
            driver=self.martijn_vd,
            team=self.martijn_vd.team,
            dna=True,
        )
        self.race2.race_entries.create(
            driver=self.bryan,
            team=self.bryan.team,
            dna=True,
        )
        self.race2.race_entries.create(
            driver=self.tim,
            team=self.tim.team,
            dna=True,
        )

    def test_leaderboard(self):
        leaderboard = self.championship.get_leaderboard()

        target_leaderboard = [
            (self.jorrick, 26),
            (self.warre, 25),
            (self.nam, 23),
            (self.martijn_vd, 20.2),
            (self.kevin, 20),
            (self.brandon, 18),
            (self.charles, 16),
            (self.jeroen, 10),
            (self.tim, 7.2),
            (self.david, 6),
            (self.bryan, 4.7),
            (self.frank, 4.7),
            (self.martijn_p, 4.7),
            (self.albion, 0),
            (self.arda, 0),
        ]

        self.assertTrue(
            leaderboard == target_leaderboard,
            "Championship.get_leaderboard() produces the wrong leaderboard.",
        )


class RaceTest(TestCase):
    def setUp(self):
        track: Track = Track.objects.create(
            location="Austria",
            name="Red Bull Ring",
            abbreviation="AUT",
            country="at",
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
            name="NAMR1 F1 Season One Championship"
        )

        self.nam: Driver = Driver.objects.create(name="Nam", team=ferrari, country="nl")
        self.warre: Driver = Driver.objects.create(
            name="Warre", team=alfa_romeo, country="be"
        )
        self.david: Driver = Driver.objects.create(
            name="David", team=mclaren, country="nl"
        )
        self.charles: Driver = Driver.objects.create(
            name="Charles", team=red_bull, country="nl"
        )
        self.jorrick: Driver = Driver.objects.create(
            name="Jorrick", team=aston_martin, country="nl"
        )
        self.frank: Driver = Driver.objects.create(
            name="Frank", team=red_bull, country="nl"
        )
        self.arda: Driver = Driver.objects.create(
            name="Arda", team=aston_martin, country="nl"
        )
        self.martijn_p: Driver = Driver.objects.create(
            name="Martijn P.", team=williams, country="nl"
        )
        self.jeroen: Driver = Driver.objects.create(
            name="Jeroen", team=ferrari, country="nl"
        )
        self.albion: Driver = Driver.objects.create(
            name="Albion", team=williams, country="nl"
        )
        self.tim: Driver = Driver.objects.create(name="Tim", team=haas, country="nl")
        self.bryan: Driver = Driver.objects.create(
            name="Bryan", team=haas, country="nl"
        )
        self.martijn_vd: Driver = Driver.objects.create(
            name="Martijn v. D.", team=alfa_romeo, country="nl"
        )
        self.brandon: Driver = Driver.objects.create(
            name="Brandon", team=alphatauri, country="nl"
        )
        self.kevin: Driver = Driver.objects.create(
            name="Kevin", team=alphatauri, country="nl"
        )

        self.race: Race = Race.objects.create(
            championship_order=1,
            championship=championship,
            track=track,
            date_time=now(),
        )

        # Finished entries
        self.race.race_entries.create(
            driver=self.warre,
            team=self.warre.team,
            dna=False,
            qualifying_position=1,
            finish_position=1,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=731),
        )
        self.race.race_entries.create(
            driver=self.martijn_vd,
            team=self.martijn_vd.team,
            dna=False,
            qualifying_position=14,
            finish_position=2,
            best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=286),
        )
        self.race.race_entries.create(
            driver=self.nam,
            team=self.nam.team,
            dna=False,
            qualifying_position=4,
            finish_position=3,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=871),
        )
        self.race.race_entries.create(
            driver=self.charles,
            team=self.charles.team,
            dna=False,
            qualifying_position=2,
            finish_position=5,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=519),
        )
        self.race.race_entries.create(
            driver=self.kevin,
            team=self.kevin.team,
            dna=False,
            qualifying_position=7,
            finish_position=6,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=772),
        )
        self.race.race_entries.create(
            driver=self.david,
            team=self.david.team,
            dna=False,
            qualifying_position=5,
            finish_position=7,
            best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=724),
        )
        self.race.race_entries.create(
            driver=self.tim,
            team=self.tim.team,
            dna=False,
            qualifying_position=3,
            finish_position=8,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=402),
        )
        self.race.race_entries.create(
            driver=self.brandon,
            team=self.brandon.team,
            dna=False,
            qualifying_position=13,
            finish_position=11,
            best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=298),
        )
        self.race.race_entries.create(
            driver=self.jorrick,
            team=self.jorrick.team,
            dna=False,
            qualifying_position=6,
            finish_position=12,
            best_lap_time=datetime.timedelta(minutes=1, seconds=6, milliseconds=750),
        )
        self.race.race_entries.create(
            driver=self.arda,
            team=self.arda.team,
            dna=False,
            qualifying_position=10,
            finish_position=12,
            best_lap_time=datetime.timedelta(minutes=1, seconds=9, milliseconds=721),
        )
        self.race.race_entries.create(
            driver=self.jeroen,
            team=self.jeroen.team,
            dna=False,
            qualifying_position=8,
            finish_position=14,
            best_lap_time=datetime.timedelta(minutes=1, seconds=7, milliseconds=962),
        )
        self.race.race_entries.create(
            driver=self.albion,
            team=self.albion.team,
            dna=False,
            qualifying_position=11,
            finish_position=15,
            best_lap_time=datetime.timedelta(minutes=1, seconds=8, milliseconds=545),
        )

        # DNA entries
        self.race.race_entries.create(
            driver=self.frank,
            team=self.frank.team,
            dna=True,
        )
        self.race.race_entries.create(
            driver=self.martijn_p,
            team=self.martijn_p.team,
            dna=True,
        )
        self.race.race_entries.create(
            driver=self.bryan,
            team=self.bryan.team,
            dna=True,
        )

    def test_get_points(self):
        points = self.race.get_points()

        target_drivers: list[tuple[Driver, int | float]] = [
            (self.nam, 15),
            (self.warre, 25),
            (self.david, 6),
            (self.charles, 10),
            (self.jorrick, 0),
            (self.frank, 2.5),
            (self.arda, 0),
            (self.martijn_p, 2.5),
            (self.jeroen, 0),
            (self.albion, 0),
            (self.tim, 5),
            (self.bryan, 2.5),
            (self.martijn_vd, 18),
            (self.brandon, 0),
            (self.kevin, 8),
        ]
        drivers_set = [e[0] for e in target_drivers]

        # Check only returns drivers who participated
        for k in points.keys():
            self.assertTrue(
                k in drivers_set,
                f"Race.get_points() returns too many drivers. Extra: {k}.",
            )

        # Check if correct points
        for (driver, target_points) in target_drivers:
            self.assertTrue(
                driver in points,
                f"Race.get_points() does not return all drivers. Missing: {driver}.",
            )
            self.assertEqual(
                points[driver],
                target_points,
                f"Race.get_points() does not return the correct points. Expected {target_points}, got {points[driver]} ({driver}).",
            )
