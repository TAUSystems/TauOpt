""" Methods for processing user inputs """

import os

def user_config_file_name(fname):
    """ extract python file name (config file) from the input string  """
    fname_parsed = fname.split(".")[0].lstrip('-').strip()
    return fname_parsed