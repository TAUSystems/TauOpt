""" Set/check input and output formats  """
from datetime import datetime

def get_time():
    """return current time in Y-m-d H:M:S format"""
    
    current_date_time = datetime.now()
    format_date_time = current_date_time.strftime("%Y-%m-%d %H:%M:%S")
    return format_date_time