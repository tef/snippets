import datetime

class London_tzinfo(datetime.tzinfo):
    """Implementation of the Europe/London timezone.
    
    Adapted from http://code.google.com/appengine/docs/python/datastore/typesandpropertyclasses.html
    https://www.gov.uk/when-do-the-clocks-change
    """
    def utcoffset(self, dt):
        return datetime.timedelta(hours=0) + self.dst(dt)

    def _last_sunday(self, dt):
        """FIX: First Sunday on or after dt."""
        return dt + datetime.timedelta(days=(6-dt.weekday()))

    def dst(self, dt):
        # 1am on the last Sunday in March
        dst_start = self._last_sunday(datetime.datetime(dt.year, 3, 8, 2))

        # back 1 hour at 2am on the last Sunday in October.
        dst_end = self._last_sunday(datetime.datetime(dt.year, 11, 1, 1))

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
