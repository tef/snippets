import datetime
import calendar

class London_tzinfo(datetime.tzinfo):
    """Implementation of the Europe/London timezone.
    
    https://www.gov.uk/when-do-the-clocks-change
    """
    def utcoffset(self, dt):
        return datetime.timedelta(hours=0) + self.dst(dt)

    def _last_sunday(self, dt):
        """First Sunday on or before  dt."""
        return dt -  datetime.timedelta(days=(1+dt.weekday())%7)

    def dst(self, dt):
        # 1am on the last Sunday in March
        last_march_day = calendar.monthrange(dt.year, 3)[1]
        dst_start = self._last_sunday(datetime.datetime(dt.year, 3, last_march_day, 1))

        # back 1 hour at 2am on the last Sunday in October.
        last_oct_day = calendar.monthrange(dt.year, 3)[1]
        dst_end = self._last_sunday(datetime.datetime(dt.year, 10, last_oct_day, 2))

        if dst_start <= dt.replace(tzinfo=None) < dst_end:
            return datetime.timedelta(hours=1)
        else:
            return datetime.timedelta(hours=0)
        
    def tzname(self, dt):
        if self.dst(dt) == datetime.timedelta(hours=0):
            return "GMT"
        else:
            return "BST"
        
        
def date_for_new_snippet():
    """Return next Monday, unless it is Monday (0) or Tuesday (1)"""
    today = now()
    if (today.weekday() < 2):
        aligned = today - datetime.timedelta(days=today.weekday())
    else:
        aligned = today + datetime.timedelta(days=(7 - today.weekday()))
    return aligned

def now():
    today = datetime.datetime.now(London_tzinfo()).date()
    return today


def date_for_retrieval():
    """Always return the most recent Monday."""
    today = now()
    return today - datetime.timedelta(days=today.weekday())
