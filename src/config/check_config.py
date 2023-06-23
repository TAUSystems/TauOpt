""" Check current configuration variables for any errors or inconsistencies """
import sys

def check_all(config):
    """ perform all checks """

    #check if the optimization varaibles are set properly
    check_opt_config(config)
    

def check_opt_config(config):
    """
    check if the optimization varaibles are set properly
    config : current configuration in config.py
    
    """

    
    if config.scan_type=='opt':

        #make sure that range of the scan parameters are set
        for v in config.var_names:
            if v not in config.var_range:
                 critical_err_config( "Optimization", 
                                      "Err: range of every scan varaible must be set ! ")
        
        #check size of the intial values
        if len(config.var_val0)<len(config.var_names):
        
             critical_err_config( "Optimization", 
                                  "Err: the initial value array (config.var0) is shorter than the number of varaibles (config.var_names) ")
        
        else:
        
            for n in range(len(config.var_names)):
                if config.var_val0[n]<config.var_range[config.var_names[n]][0] or config.var_val0[n]>config.var_range[config.var_names[n]][1]:
                   
                    critical_err_config( "Optimization",
                                         "Err: out of bound initial value ")



def critical_err_config(type,msg):
    
    """ display the error message and exit"""

    print(f" Configuration error  :: {type} \n")
    print(msg)
    sys.exit()