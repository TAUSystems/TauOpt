""" Write input parameters in input files / source code """

import os
from ..config import config
from ..util import gbl_vars


def write_new_param_into_setup_file(sim_num):
    """
    Write input parameters (var_names) for simulation number "sim_num" into files (input_files)
    """

    dest_folder= os.path.join(config.project_folder, 'run'+str(sim_num)) 

    for n in range(len(config.input_file)):
        try:
            with open(dest_folder+'/'+config.input_file[n],"r") as f: 
                fdata = f.read()
            
            for v in config.var_names: 
                fdata = fdata.replace(config.var_names_prefix+str(v),str(gbl_vars.run_info['run'+str(sim_num)][v]))

            with open(dest_folder+'/'+config.input_file[n],"w") as f:
                f.write(fdata)
        except:
            pass
