""" Checks at startup """

import os
import sys
from ..config import config


def check_project_folder_path():

    if not os.path.isdir(config.project_folder):
        
        # check if the executable exists
        if not os.path.isfile(config.exec_name):
            print(f" 'project_folder' = {config.project_folder}")
            print(f" The folder does not exist. Please specify a correct path in the configuration file. ")

            msg =  """
                    If the project folder does not exist, it is created only if the executable is \n 
                    a standard file (must exist and its full path must be provided in the user config. file \n
                    Note: in this case the executable is not copied between runs.  \n """
            
            print(f"{msg}")
            sys.exit()
