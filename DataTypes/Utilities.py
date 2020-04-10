import sys;
import datetime;
import time;

def convertToLocalDate(val):
    """
    Description:
        This method will convert the value received from the lynx, which
        is a Win32 FILETIME struct, into a localized Python date/time
    Arguments:
        val    (in, double or long) The value to convert
    Returns:
        (datetime) The converted value
    """
    _FILETIME_null_date = datetime.datetime(1601, 1, 1, 0, 0, 0)
    timestamp = long(val)
    val= _FILETIME_null_date + datetime.timedelta(microseconds=timestamp/10) - datetime.timedelta(seconds=time.timezone)
    if (1==time.daylight):
        val += datetime.timedelta(seconds=3600)
    return val
def convertToLynxDate(val):
    """
    Description:
        This method will convert the argument to a Lynx date/time value
    Arguments:
        val    (in, datetime) The value to convert
    Returns:
        (long) The converted value
    """
    _FILETIME_null_date = datetime.datetime(1601, 1, 1, 0, 0, 0)
    res = val-_FILETIME_null_date + datetime.timedelta(seconds=time.timezone)
    if (1==time.daylight):
        res -= datetime.timedelta(seconds=3600)
    return res.microseconds*10;    
                        