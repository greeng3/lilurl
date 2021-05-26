"""
For a scalable solution, we would want a redundant external database so that there would be both
long-term persistence (until some expiration date), and to keep the service functional in
the face of an outage.  Also, keeping the data external to the app allows multiple copies to be
run to service higher traffic without short URL collisions.

To keep things in the time frame, and knowing that for testing, the amount of data this
will actually have to hold is small, a dummy database will be used here.
"""

from datetime import datetime


class DatabaseWrapper:
    def __init__(self):
        # original URLs, indexed by the short URL
        # So, if someone asks for the short version of a URL we've already shortened, they
        # get the same one
        self.__url_to_short = {}

        # short URLs, indexed by the original URL
        # Used for the 301 Redirect to the original URL
        self.__short_to_url = {}

        # [("short URL", timestamp)]
        # The idea is to be able to expire pairs older than a certain age.
        self.__timestamps = []

    def add(self, url, short):
        """
        not checking for collisions here, but if we got the short version through some
        sort of hash, we'd want to.
        """
        self.__url_to_short[url] = short
        self.__short_to_url[short] = url

        stamped = short, datetime.utcnow()
        self.__timestamps.append(stamped)

        print(f"Added: {url} as {short} at {stamped[1]}")

    def lookup_url(self, url):
        """
        returns the short version of URL, or None if we don't have it
        """
        return self.__url_to_short.get(url, None)

    def lookup_short(self, short):
        # returns the long version of a shortened URL, or None if we don't have it
        return self.__short_to_url.get(short, None)

    def expire(self, age):
        """
        age is a timedelta, so we look for the index of the most recent item that's too old
        This could be run on a timer, whenever add is called, every N calls to add, or 
        whatever keeps up, but doesn't make too much of a performance hit.
        """
        too_old = datetime.utcnow - age

        if self.__timestamps[0][1] <= too_old:
            # everything is too stale, so throw it all away
            self.__url_to_short = {}
            self.__short_to_url = {}
            self.__timestamps = []
            return

        if self.__timestamps[-1][1] > too_old:
            # nothing is expired
            return

        # Some items are expired, so delete them in a sensible order
        index = self.__find_first_unexpired_index(age)
        for short, _ in self.__timestamps[:index]:
            url = self.__short_to_url[short]
            del self.__short_to_url[short]
            del self.__url_to_short[url]
        self.__timestamps = self.__timestamps[index:]

    def __find_first_unexpired_index(self, age):
        """
        TODO Taking a binary search for the index as given, in the interest of time
        """
        return len(self.__timestamps)

    def braindump(self):
        print("url_to_short")
        for k, v in self.__url_to_short.items():
            print(f"    {k}: {v}")
        print("short_to_url")
        for k, v in self.__short_to_url.items():
            print(f"    {k}: {v}")
        print("timestamps")
        for ts in self.__timestamps:
            print(f"    {ts}")
