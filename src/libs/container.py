# Copyright 2020 Kinvolk GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# NOTE: This library is use to clarify the corresponding container of 
# current task. 
# Modified: PHUCDT
# Ref: Kinvolk GmbH - 
# In the hook function use 
#   if (container_should_be_filtered()) {
#        return 0;
#    }
# For checking the filtering container

def _cgroup_filter_func_writer(cgroupmap):
    if not cgroupmap:
        return """
        static inline int _cgroup_filter() {
            return 0;
        }
        """

    text = """
    
    /*
     * Return directly the result of comparison between cgroupid
     * and cgroupmap which in u32 hex number
     */
    static inline int _cgroup_filter() {
        u64 cgroupid = bpf_get_current_cgroup_id();
        return cgroupid == CGROUP_PATH;
    }
    """

    return text.replace('CGROUP_PATH', cgroupmap)

def _mntns_filter_func_writer(mntnsmap):
    if not mntnsmap:
        return """
        static inline int _mntns_filter() {
            return 0;
        }
        """
    text = """
    #include <linux/nsproxy.h>
    #include <linux/mount.h>
    #include <linux/ns_common.h>

    struct mnt_namespace {
    // This field was removed in https://github.com/torvalds/linux/commit/1a7b8969e664d6af328f00fe6eb7aabd61a71d13
    #if LINUX_VERSION_CODE < KERNEL_VERSION(5, 11, 0)
        atomic_t count;
    #endif
        struct ns_common ns;
    };
    /*
     * Return directly the result of comparison between ns.inum 
     * and mnynsmap which in u32 hex number
     */
    #define MNT_NAMESPACE_DEFINED

    static inline int _mntns_filter() {
        struct task_struct *current_task;
        struct nsproxy *nsproxy;
        struct mnt_namespace *mnt_ns;
        unsigned int inum;

        current_task = (struct task_struct *)bpf_get_current_task();
        if (bpf_probe_read_kernel(&nsproxy, sizeof(nsproxy), &current_task->nsproxy))
            return 0;
        if (bpf_probe_read_kernel(&mnt_ns, sizeof(mnt_ns), &nsproxy->mnt_ns))
            return 0;
        if (bpf_probe_read_kernel(&inum, sizeof(inum), &mnt_ns->ns.inum))
            return 0;
        return inum == MOUNT_NS_PATH;
    }
    """

    return text.replace('MOUNT_NS_PATH', mntnsmap)

# For more concrete
def filter_by_containers(cgroupmap, mntnsmap):
    # Return a bcc code that make the program filtering the container 
    # based on its cgroupmap (Cgroup ID) and mntsmap (Mount NS ID)

    # filter_by_containers_text = """
    # static inline int container_should_be_filtered() {
    #     return _cgroup_filter() || _mntns_filter();
    # }
    # """

    filter_by_containers_text = """
    static inline int container_should_be_filtered() {
        return _mntns_filter();
    }
    """

    # cgroupmap_text = _cgroup_filter_func_writer(cgroupmap)
    mntnsmap_text = _mntns_filter_func_writer(mntnsmap)

    # return cgroupmap_text + mntnsmap_text + filter_by_containers_text
    return  mntnsmap_text + filter_by_containers_text