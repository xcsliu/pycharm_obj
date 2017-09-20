import pandas as pd

from xkool_site.components.poi.util import get_data_file_path
from xkool_site.util.xkool_date_util import XkDateUtil


def get_today_golden_data(city_name):
    xkool_date = XkDateUtil()
    ready_data_file_path = get_data_file_path(city_name,
                                              xkool_date.today_string)
    ready_data = pd.read_table(ready_data_file_path, error_bad_lines=False)
    return ready_data






