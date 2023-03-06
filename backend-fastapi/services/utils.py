
import datetime
import pytz


def convert_unix_time(unix_time):
    utc_datetime = datetime.datetime.utcfromtimestamp(unix_time)
    gmt5_tz = pytz.timezone("America/Bogota")
    gmt5_datetime = utc_datetime.astimezone(gmt5_tz)
    return utc_datetime, gmt5_datetime



