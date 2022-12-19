# Moises Shalimay S Andrade
# This is an auxiliary module to deal with datetime validation, conversion and arithmetics

from myNumbers import *
import datetime
import dateutil
from dateutil.tz import tzlocal, UTC, tzrange
import pytz
from tzlocal import get_localzone, get_localzone_name
from zoneinfo import ZoneInfo

def valid_date(date:str, remove_whitespace=False, dt_format="%m/%d/%Y"):
    """ Checks if string can be represented as a datetime object and returns a boolean
    Args:
        date (str): A string potentially convertible to a python datetime object
        dt_format (str): the format day/month/year format of the date the string is representing
        remove_whitespace: remove whitespaces before checking?  
    """       

    if remove_whitespace:
        date = date.strip()

    # if able to convert the string to a python datetime in the passed format, string is date, True; else, False
    try:
        datetime.datetime.strptime(date, dt_format)
        return True
    except:
        return False

def date_localtz(date_naive:str):
    """ Tries to retrieve the user's system local timezone and assigns it to a naive datetime object

    Args: date_naive (datetime): a datetime object without tzinfo
    
    Returns: date (datetime): If successful, aware datetime object with tzinfo = user's system local time; returns back 'date_naive' 
    """

    # Local timezone retrievement might be affected by the user OS, python version, personal configurations, etc.
    # Until latest releases of 'dateutil' (as of 2022), no direct method existed to retrieve this information. Some python versions might not be supported by this method.
    # Therefore, implementation strategy: tries to retrieve user local timezone through three methods.
     
    try:
        # method 1: 'dateutil' direct method (PEP 495 compatible, 2020)
        date = date_naive.replace(tzinfo=tzlocal())
        return date
    except:
        try:
            print("\nUnable to convert with dateutils. Trying with pytz method.\n")

            # method 2: pytz + localize (previous to PEP 495)

            # retrieves pytz object through 'tzlocal.get_localzone()' method. Obs.: might not be able to correctly identify the timezone used by the OS
            local_tzinfo = get_localzone()

            # turns the date_naive object aware to the timezone in 'local_tzinfo' through pytz.localize(...)
            date = local_tzinfo.localize(date_naive)
            return date

        except:
            print("\nUnable to convert with with pytz method. Trying with datetime method\n")
            try:
                # method 3: timezone replace (previous to PEP 495). Less robust to date arithmetics and conversions

                # computes the datetime from current time and retrieves its timezone info
                    # obs.: this dont work: date = datetime.datetime.now(); date.astimezone().tzinfo 
                    #       it seems that when a datetime.datetime.now() is assigned to a variable, it is assigned as naive date
                        
                local_tzinfo = datetime.datetime.now().astimezone().tzinfo
                # replace the naive_object tzinfo by local_tzinfo
                date = date_naive.replace(tzinfo=local_tzinfo)
                return date
            except:
                # no method worked, return original date
                print("\nUnable to convert include timezone. Returning the original date.\n")
                return date_naive


def date_diff_absolute(dt1, dt2):
    """ Compute timedelta of dates with potentially different timezones by converting and doing arithmetic in UTC time 
    Args:
        dt1, dt2 (datetime): Aware datetime objects with tzinfo potentially different from each other
    Returns:
        timedelta: a timedelta with the time difference in absolute terms
    """
    dt1 = dt1.astimezone(UTC)
    dt2 = dt2.astimezone(UTC)
    tdelta = dt1-dt2
    return tdelta


#=====================================================================================
#SECTION Working on
#=====================================================================================


def abbreviate_tz(tz_name, max_len = 10, desired_len = 5):
    #TODO creating a list of abbreviations and pass to the 'tzinfos' argument
    # seems the best solution.
    # Resources: https://www.timeanddate.com/time/zones/, https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations, https://stackoverflow.com/questions/1703546/parsing-date-time-string-with-timezone-abbreviated-name-in-python
    new_name = ""
    tz_name_strip = tz_name.strip().split()

    if desired_len > max_len:
        print("Timezone length already less than desired length")
        return tz_name
    if len(tz_name) > max_len:
        j=0
        while True:
            for i in range(len(tz_name_strip)):    
                if j <= len(tz_name_strip[i]):
                    if tz_name_strip[i][j].isalpha():
                        new_name+= tz_name_strip[i][j]
                if len(new_name)>= desired_len:
                    return new_name
            j = j+1
            

    
    
#\SECTION

#=====================================================================================
#SECTION DEPRECATED
#=====================================================================================
def valid_day(day, min_day = 1, max_day= 31):
    if str_is_integer(day,False,False):
        day = int(day)
        if day >= min_day and day <= max_day:
            return True
    return False

def valid_month(month, min_month = 1, max_month= 12):
    if str_is_integer(month,False,False):
        month = int(month)
        if month >= min_month and month <= max_month:
            return True       
    return False


def valid_year(year, min_year = 0, max_year= 99999):
    if str_is_integer(year,False,False):
        year = int(year)
        if year >= min_year and year <= max_year:
            return True       
    return False


#def date_localtz(date_naive:str):
#    """ for further reference, documentation of the methods to retrieve the local user timezone
#    1: pytz.localize + tzlocal
#        - it seems this is a more robust solution to do arithmetics with the dates
#        - problem: difficult to convert the date back to the local user standard without providing it excplictly as below
#            - local_tzinfo = pytz.timezone("America/Sao_Paulo")
#        - Solution is using 'getlocal()' from the tzlocal package (tries to return a py.tz timezone object in line with the local timezone of the user's PC)
#        - Problem: it seems 'tzlocal' is not consistent to many python versions. Have to error handle it better
#        - Warning: it doesnt work perfectly with the time formmating from the native datetime module; 
#        for instance, in example below, the timezone name returned should be the string "America/Sao_Paulo", but instead it returns '-03' (which is th utcoffset)
#
#            local_tzinfo = get_localzone()
#            date = local_tzinfo.localize(date_naive)
#            datetime.datetime.strftime(date, "%Z") -> error
#    """
#    pass