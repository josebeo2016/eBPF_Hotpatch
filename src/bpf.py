import logging
import libs.container as container
import libs.utils as utils
import libs.yamlrule as yamlrule
import re
import config
from bcc import BPF
import datetime

import time
import os, psutil

logger = logging.getLogger("log")
containerID = ""
def load_bpf_prog(name, params):
    '''
    name: lsm_probe name
    params: is a dictionary which contain:
        key: name of the param to replace in bpf_prog
        value: the value that need to replace
        Note: if the key is not disappeared in the bpf_prog, then do nothing
              if there are more key in the bpf_prog, then return params will contain
              the list of params left (not shown in params)
    Return: (str: bpf_prog, list: params_left)
    '''
    raw = ""
    res = ""
    
    with open(config.bpf_prog_dir + name + ".c", "r") as file:
        raw = file.read()
    # GET bpf_prog supported params
    lsm_params = re.compile(r'\* params: (.*$)',flags=re.I|re.M).findall(raw)[0].strip().split(',')
    logger.debug("Params required by LSM probe: {}".format(lsm_params))
    params_left = lsm_params
    # Replace params:
    for k,v in params.items():
        logger.debug("key {} value {}".format(k,v))
        if(k in lsm_params):
            params_left = params_left.remove(k)
        raw = raw.replace(k,v)
    
    logger.debug(raw)

    return raw, params_left

def run(args):
    #### Get mntns ID and cgroup ID
    # TODO: Cgroup ID is not available yet
    ##############################################
    # Get inode from file (-F) and --dockerid 
    ##############################################
    process = psutil.Process(os.getpid())   

    start_time = time.time()
    
    if(args.inode):
        if (args.fullpath==None or args.dockerid == None):
            logger.error("Please provide Docker ID and Target file for conversion")


        inode = utils.path2inode(args.fullpath,args.dockerid)    
        logger.debug("Inode of file {} is {}".format(args.fullpath,inode))
        print(inode)
        return inode
    

    mntns = "0xffffffff"
    if (args.namespace):
        mntns = args.namespace
    elif (args.pid):
        mntns = utils.contaierID_2_cgroup_mntns(args.pid, isPID=True)
    elif (args.dockerid):
        mntns = utils.contaierID_2_cgroup_mntns(args.dockerid, isPID=False)
    else:
        logger.error("Please provide Namespace ID or Container PID")
    # params = {
    #     "DATA_T_MORE_INFORMATION":"", 
    #     "MOUNT_NS_ID":mntns,
    #     "CONDITIONS":"1", 
    #     "ACTION":"0"
    # }
    
    # Load rule
    if (args.file):
        yaml_data = yamlrule.load(args.file)
        lsm_hook, params = yamlrule.loadrule(yaml_data)
    
    if (lsm_hook==None or params == None):
        logger.error("lsm_hook or params should not be None")
        return -1
    # Add mntns to params:
    params['MOUNT_NS_ID'] = mntns

    # Make bpf_prog
    bpf_prog, params = load_bpf_prog(name = lsm_hook,params=params)
    
    # Check params
    if (params is not None):
        logger.error("There are some params left in the program need to be filled! \n {}".format(params))
        return -1
    containerID = args.dockerid
    logger.info("Preprocessing time: {}".format(time.time()-start_time))
    
    process = psutil.Process(os.getpid())
    mem_before = process.memory_info().rss
    
    # time.sleep(5)
    logger.info("Start attaching patch!")
    start_time = time.time()
    b = BPF(text=bpf_prog)
    logger.info("Attaching time: {}".format(time.time()-start_time))
    
    process = psutil.Process(os.getpid())
    logger.info("Memory usage: {}".format(process.memory_info().rss - mem_before))  # in bytes 
    
    def print_event(cpu, data, size):
        """
        Print event data when a kill signal is about to be
        sent.
        """
        event = b["events"].event(data)
        print(
            datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S"), " [{}] ".format(lsm_hook), utils.all_event(event)
        )
        
        if(event.is_vuln):
            print("Vulnerability Detected! Stop the trigger")
            utils.kill_task(event.pid)
            # utils.kill_container(containerID)
        

    b["events"].open_perf_buffer(print_event)
    while 1:
        try:
            b.perf_buffer_poll()
        except KeyboardInterrupt:
            # calculate attach time
            # start_time = time.time()
            # b.detach_kprobe(event="cgroup_release_agent_write")
            # logger.info("Detaching time: {}".format(time.time()-start_time))
            exit()


    #### 


    