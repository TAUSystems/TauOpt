""" Write output files """

import os
import json
from ..util import gbl_vars
from ..config import config

def write_param(sim_num):
    param_file = config.project_folder+'/'+'run'+str(sim_num)+"/tau_opt/param.json"
    if not os.path.isfile(param_file):
        param = {}
        for v in config.var_names:
            param[v] = gbl_vars.run_info['run'+str(sim_num)][v]
        with open(param_file,"w") as file:
            json.dump(param,file,indent=4)    