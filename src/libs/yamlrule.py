import yaml
from yaml.loader import SafeLoader
import logging

logger = logging.getLogger("log")


def load(file):
    with open(file) as f:
        try:
            data = yaml.load(f, Loader=SafeLoader)
            logger.debug("rule: {}".format(data))
            return data
        except:
            logger.error("Error in load yaml rule")

def loadrule(yaml_data):
    try:
        if(yaml_data['Action'].lower() == 'deny'):
            action = "-1";
            inverse = "0";
        elif(yaml_data['Action'].lower() == 'allow'):
            action = "0";
            inverse = "-1";
        else:
            logger.error("The current version only support for allow and deny Action.")
            return None, None
        condition = yaml_data['Condition'].strip()
        moreInfo = yaml_data['More_Info'].strip()
        lsm_probe = yaml_data['LSM_Probe'].strip()
    except:
        logger.error("Required key(s) is not existed. Please check the document.")
        return None, None
    params = {
        "DATA_T_MORE_INFORMATION":moreInfo, 
        "MOUNT_NS_ID":"",
        "CONDITIONS":condition, 
        "ACTION":action,
        "INVERSE": inverse
    }
    return lsm_probe, params


