import unittest
import datetime
from skyfield.api import Topos, Loader, wgs84
from skyfield import almanac
from pprint import pprint
from skyfield import eclipselib
from pytz import timezone

load = Loader("/var/data")
ephemeris = load('de406.bsp')
ts = load.timescale()

us_states_and_territories = {
    # state, first year voting in federal elections, timezone, capital coordinates
    'Alabama': {'year': 1820, 'tz': 'US/Central', 'lat': 32.377716, 'lon': -86.300568},
    'Alaska': {'year': 1959, 'tz': 'America/Anchorage', 'lat': 58.301598, 'lon': -134.420212},
    'American Samoa': {'year': 1900, 'tz': 'Pacific/Samoa', 'lat': -14.2710, 'lon': -170.1322},
    'Arizona': {'year': 1912, 'tz': 'US/Mountain', 'lat': 33.448143, 'lon': -112.096962},
    'Arkansas': {'year': 1836, 'tz': 'US/Central', 'lat': 34.746613, 'lon': -92.288986},
    'California': {'year': 1850, 'tz': 'US/Pacific', 'lat': 38.576668, 'lon': -121.493629},
    'Colorado': {'year': 1876, 'tz': 'US/Mountain', 'lat': 39.739227, 'lon': -104.984856},
    'Connecticut': {'year': 1788, 'tz': 'US/Eastern', 'lat': 41.764046, 'lon': -72.682198},
    'Delaware': {'year': 1788, 'tz': 'US/Eastern', 'lat': 39.157307, 'lon': -75.519722},
    'Florida': {'year': 1845, 'tz': 'US/Eastern', 'lat': 30.438118, 'lon': -84.281296},
    'Georgia': {'year': 1788, 'tz': 'US/Eastern', 'lat': 33.749027, 'lon': -84.388229},
    'Hawaii': {'year': 1959, 'tz': 'US/Hawaii', 'lat': 21.307442, 'lon': -157.857376},
    'Idaho': {'year': 1890, 'tz': 'US/Mountain', 'lat': 43.617775, 'lon': -116.199722},
    'Illinois': {'year': 1820, 'tz': 'US/Central', 'lat': 39.798363, 'lon': -89.654961},
    'Indiana': {'year': 1817, 'tz': 'US/Eastern', 'lat': 39.768623, 'lon': -86.162643},
    'Iowa': {'year': 1847, 'tz': 'US/Central', 'lat': 41.591087, 'lon': -93.603729},
    'Kansas': {'year': 1861, 'tz': 'US/Central', 'lat': 39.048191, 'lon': -95.677956},
    # eastern half was settled first, going with EST
    'Kentucky': {'year': 1792, 'tz': 'US/Eastern', 'lat': 38.186722, 'lon': -84.875374},
    'Louisiana': {'year': 1812, 'tz': 'US/Central', 'lat': 30.457069, 'lon': -91.187393},
    'Maine': {'year': 1820, 'tz': 'US/Eastern', 'lat': 44.307167, 'lon': -69.781693},
    'Maryland': {'year': 1788, 'tz': 'US/Eastern', 'lat': 38.978764, 'lon': -76.490936},
    'Massachusetts': {'year': 1788, 'tz': 'US/Eastern', 'lat': 42.358162, 'lon': -71.063698},
    'Michigan': {'year': 1837, 'tz': 'US/Eastern', 'lat': 42.733635, 'lon': -84.555328},
    'Minnesota': {'year': 1858, 'tz': 'US/Central', 'lat': 44.955097, 'lon': -93.102211},
    'Mississippi': {'year': 1817, 'tz': 'US/Central', 'lat': 32.303848, 'lon': -90.182106},
    'Missouri': {'year': 1821, 'tz': 'US/Central', 'lat': 38.579201, 'lon': -92.172935},
    'Montana': {'year': 1889, 'tz': 'US/Mountain', 'lat': 46.585709, 'lon': -112.018417},
    'Nebraska': {'year': 1867, 'tz': 'US/Central', 'lat': 40.808075, 'lon': -96.699654},
    'Nevada': {'year': 1864, 'tz': 'US/Pacific', 'lat': 39.163914, 'lon': -119.766121},
    'New Hampshire': {'year': 1788, 'tz': 'US/Eastern', 'lat': 43.206898, 'lon': -71.537994},
    'New Jersey': {'year': 1788, 'tz': 'US/Eastern', 'lat': 40.220596, 'lon': -74.769913},
    'New Mexico': {'year': 1912, 'tz': 'US/Mountain', 'lat': 35.68224, 'lon': -105.939728},
    'New York': {'year': 1788, 'tz': 'US/Eastern', 'lat': 42.652843, 'lon': -73.757874},
    'North Carolina': {'year': 1788, 'tz': 'US/Eastern', 'lat': 35.78043, 'lon': -78.639099},
    'North Dakota': {'year': 1889, 'tz': 'US/Central', 'lat': 46.82085, 'lon': -100.783318},
    'Ohio': {'year': 1803, 'tz': 'US/Eastern', 'lat': 39.961346, 'lon': -82.999069},
    'Oklahoma': {'year': 1908, 'tz': 'US/Central', 'lat': 35.492207, 'lon': -97.503342},
    'Oregon': {'year': 1859, 'tz': 'US/Pacific', 'lat': 44.938461, 'lon': -123.030403},
    'Pennsylvania': {'year': 1788, 'tz': 'US/Eastern', 'lat': 40.264378, 'lon': -76.883598},
    'Rhode Island': {'year': 1790, 'tz': 'US/Eastern', 'lat': 41.830914, 'lon': -71.414963},
    'South Carolina': {'year': 1788, 'tz': 'US/Eastern', 'lat': 34.000343, 'lon': -81.033211},
    # Eastern part was settled first
    'South Dakota': {'year': 1889, 'tz': 'US/Central', 'lat': 44.367031, 'lon': -100.346405},
    # EasEasternrtern part was settled first
    'Tennessee': {'year': 1796, 'tz': 'US/Eastern', 'lat': 36.16581, 'lon': -86.784241},
    'Texas': {'year': 1846, 'tz': 'US/Central', 'lat': 30.27467, 'lon': -97.740349},
    'Utah': {'year': 1896, 'tz': 'US/Mountain', 'lat': 40.777477, 'lon': -111.888237},
    'Vermont': {'year': 1791, 'tz': 'US/Eastern', 'lat': 44.262436, 'lon': -72.580536},
    'Virginia': {'year': 1788, 'tz': 'US/Eastern', 'lat': 37.538857, 'lon': -77.43364},
    'Washington': {'year': 1890, 'tz': 'US/Pacific', 'lat': 47.035805, 'lon': -122.905014},
    'West Virginia': {'year': 1863, 'tz': 'US/Eastern', 'lat': 38.336246, 'lon': -81.612328},
    'Wisconsin': {'year': 1848, 'tz': 'US/Central', 'lat': 43.074684, 'lon': -89.384445},
    'Wyoming': {'year': 1890, 'tz': 'US/Mountain', 'lat': 41.140259, 'lon': -104.820236},
}


def find_first_dow(year, month, dow):
    '''
    finds the date of the first date of the given day of the week
    :param year: year
    :param month: month
    :param dow: day of the week, 0 = Sunday
    :return:
    '''
    d = datetime.datetime(year, int(month), 1, tzinfo=datetime.timezone.utc)
    jlk = d.weekday()
    offset = dow - d.weekday()  # weekday = 0 means monday
    if offset < 0:
        offset += 7
    return d + datetime.timedelta(offset)


def lunar_eclipses_on_election_day(firstyear=1789, lastyear=2999, types=['Total', 'Partial', 'Penumbral']):
    '''
    calculate lunar eclipses
    :param firstyear: first presidential election
    :param lastyear: last year available the ephemeris, for de406 this is 3000
    :return: list of strings with the type of the eclipse, day of the week, date, and timezone
    '''
    lines = []
    t0 = ts.utc(firstyear, 1, 1)
    t1 = ts.utc(lastyear, 12, 31)
    t, y, details = eclipselib.lunar_eclipses(t0, t1, ephemeris)  # mid eclipse time
    for ti, yi in zip(t, y):
        utc = ti.utc_datetime()
        year = utc.year
        if year < 1880 and year % 2 == 1 and year != 1789:
            continue  # elections where held on even years prior to 1880
        if utc.month < 10:
            continue
        eclipse_type = eclipselib.LUNAR_ECLIPSES[yi]

        if eclipse_type not in types:
            continue

        visible_times = set()
        for state, data_state in us_states_and_territories.items():
            tz = timezone(data_state['tz'])
            if year < data_state['year']:
                continue  # not yet admitted to the union
            first_day, last_day = election_days(tz, utc.year)
            eclipse_local_time = utc.astimezone(tz).replace(tzinfo=None)
            if first_day <= eclipse_local_time and eclipse_local_time <= last_day:
                altitude = moon_above_horizon(data_state['lat'], data_state['lon'], ti)
                if altitude > 0:
                    tzcode = utc.astimezone(tz).strftime('%Z')
                    if tzcode == 'LMT':  # Local Mean Time, before timezones
                        visible_times.add(f"{eclipse_type:10} {utc.astimezone(tz).strftime('%a %Y-%m-%d')}")
                    else:
                        visible_times.add(f"{eclipse_type:10} {utc.astimezone(tz).strftime('%a %Y-%m-%d %H:%M %Z')}")
        lines += sorted(list(visible_times))
    return lines


def election_days(tz, year):
    '''
    find the days ballots were cast based on the year
    :param tz: timezone object
    :param year: election year
    :return: first minute of the first day of voting, last minute of the last day of voting
    '''
    if year < 1845:  # election day act passed
        last_day = find_first_dow(year, 12, 2)  # first wednesday in Dec
        first_day = last_day - datetime.timedelta(days=34)
    else:
        first_day = find_first_dow(year, 11, 0) + datetime.timedelta(days=1)
        last_day = first_day
    first_day = first_day.replace(tzinfo=None)
    last_day = last_day.replace(tzinfo=None)
    last_day = last_day.replace(hour=23, minute=59)
    return first_day, last_day


def moon_above_horizon(lat, lon, t):
    ''' calculates the altitude (in degrees) of the moon from given latitude and longitude at a given time

    :param lat: latitude (float), negative for south
    :param lon: longitude (float), negative for west
    :param t: Skyfield time object
    :return: altitude in degrees (float)
    '''
    topo = ephemeris['earth'] + wgs84.latlon(lat, lon)
    astro = topo.at(t).observe(ephemeris['moon'])
    app = astro.apparent()
    alt, az, distance = app.altaz()
    return alt.degrees


class MyTestCase(unittest.TestCase):
    def test_2022(self):
        lines = lunar_eclipses_on_election_day(firstyear=2022, lastyear=2023)
        self.assertEqual(len(lines), 6)
        print("\n".join(lines))

    def test_1846_2022(self):
        lines = lunar_eclipses_on_election_day(firstyear=1778, lastyear=2022)
        self.assertEqual(len(lines), 12)

    def test_2022_3000(self):
        lines = lunar_eclipses_on_election_day(firstyear=2023, lastyear=2999)
        self.assertEqual(len(lines), 36)

    def test_first_tues(self):
        first_tues_2022 = find_first_dow(2022, 11, 0) + datetime.timedelta(days=1)
        self.assertEqual(first_tues_2022.day, 8)
        first_tues_2021 = find_first_dow(2021, 11, 0) + datetime.timedelta(days=1)
        self.assertEqual(first_tues_2021.day, 2)


if __name__ == '__main__':
    lines = lunar_eclipses_on_election_day()
    print(f"lunar eclipses on election day\n{'-' * 40}")
    prevyear = ''
    for line in lines:
        year = line[15:19]
        atoms = line.split()
        if prevyear != year:
            print(f"\n* {line[:25]}", end=' ')
        if prevyear == year:
            print(atoms[-1], end=' ')

        prevyear = year
