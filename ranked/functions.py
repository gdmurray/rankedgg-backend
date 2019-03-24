import datetime
import pytz


def timedelta_now_hours(dt):
    now = datetime.datetime.now(tz=pytz.UTC)
    seconds = (now - dt).total_seconds()
    hours = seconds // 3600
    # print("Comparing Dates: ", now, dt, hours)
    return hours
