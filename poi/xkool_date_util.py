import datetime


class XkDateUtil(object):
    def __init__(self, format="%Y_%m_%d"):
        self.format = format

    @property
    def today(self):
        return datetime.date.today()

    @property
    def yesterday(self):
        return self.today - datetime.timedelta(days=1)

    @property
    def today_string(self):
        return self.today.strftime(self.format)

    @property
    def yesterday_string(self):
        return self.yesterday.strftime(self.format)