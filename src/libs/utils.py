# -*- coding: utf-8 -*-
import logging
import os
from pprint import pformat
from stat import S_ISREG, S_ISDIR
from requests import request
import subprocess
from bcc import BPF
from time import sleep
import yaml


logger = logging.getLogger("log")

def mkpdirs(path):
    if not os.path.isdir(path):
        os.makedirs(path)

def request_and_check(method, url, **kwargs):
    logger.debug('%s: %s with parameters: %s', method, url, pformat(kwargs))
    resp = request(method, url, **kwargs)
    logger.debug('Response: %s', resp)
    resp.raise_for_status()
    return resp

def run_cmd(cmd,timeout=300):
    try:
        process = subprocess.check_output(cmd, shell=True,timeout=timeout)
        # out, error = process.communicate(timeout=200)
        return process.decode('utf-8').strip()
    except Exception as e:
        return "ERROR {}".format(e).strip()

def run_cmd_with_err(cmd,timeout=300):
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    out, error = process.communicate(timeout=timeout)
    return out.decode('utf-8').strip(),error.decode('utf-8').strip()
        
def read_file(file):
    with open(file,"r",encoding="utf-8") as f:
        return f.readlines()


### NOTE: ContainerID need to be validated
def contaierID_2_cgroup_mntns(contaierID, isPID=False):
    '''
    Params: 
    - containerID: could be docker contaienr ID or 
    PID in string type
    - isPID: True: containerID is PID string
    
    Return cgroup ID and mntns ID as hex string,
    u32 hex string
    else "0" if error occurs or "" if no ID found
    TODO: Cgroup ID is not available yet
    '''


    cgroupID = ""
    mntnsID = ""
    # Get PID of the container
    if (not isPID):
        pid = containerID_2_PID(contaierID)
    else:
        pid = contaierID
    if (pid == '-1'):
        return "0","0"
    cmd = "stat -Lc '%i' /proc/"+pid+"/ns/mnt"
    cmd = cmd.split(" ")
    try:
        out = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        logger.error(e)
        out = b'0'
    mntnsID = hex(int(out.strip().decode("utf-8").replace("'",""),base=10))
    return mntnsID

def containerID_2_PID(containerID):
    # Return PID as string, else -1 if error occurs
    cmd = "docker inspect -f '{{.State.Pid}}' %s" %(containerID)
    cmd = cmd.split(" ")
    try:
        out = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        logger.error(e)
        out = b'-1'
    return out.strip().decode("utf-8").replace("'","")

def all_event(data, l=None):
    res = ""
    if l==None:   
        for i in dir(data):
            if (not i.startswith('_')):
                res += "{}={} ".format(i,getattr(data,i))
    else:
        for i in l:
            res += "{}={} ".format(i,getattr(data,i))
    return res


############################
def path2inode(path, containerID):
    container_merged, error = run_cmd_with_err("docker inspect {containerID} --format='{{json .GraphDriver.Data.MergedDir}}'")
    container_merged = container_merged.strip()[1:-1]
    real_path = container_merged + "/" + path
    inode = os.stat(real_path).st_ino
    return inode

############################
def kill_container(containerID):
    output, error = run_cmd_with_err("docker stop {}".format(containerID))
    print(output, error)
    return True

def kill_task(pid):
    output, error = run_cmd_with_err("kill -9 {}".format(pid))
    print(output, error)
    return True