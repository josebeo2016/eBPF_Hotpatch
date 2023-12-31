/* ################################
 * static inline int security_path_mkdir
 * Author: PHUCDT
 * Date: 11/5/2021
 * Params: DATA_T_MORE_INFORMATION, MOUNT_NS_ID, CONDITIONS, ACTION, INVERSE_ACTION
 * CVE-2022-0185
 * ################################
 */
#include <linux/security.h>

#include <linux/nsproxy.h>
#include <linux/mount.h>
#include <linux/ns_common.h>

#include <linux/errno.h>
#include <linux/fs.h>
#include <linux/path.h>

#include <linux/kernfs.h>
#include <linux/capability.h>
#include <linux/fs.h>
#include <linux/cgroup.h>
#include <trace/events/cgroup.h>
#include <linux/cgroupstats.h>

#include <linux/fs_context.h>

#define __LOWER(x) (x & 0xffffffff)
#define __UPPER(x) (x >> 32)
#define MAX_LENGTH 128

/*
 * Create a data structure for collecting event data
 */
struct data_t {
    char comm[TASK_COMM_LEN];
    u32 uid;
    u32 gid;
    u32 pid;
    u32 target_pid;
    u32 is_vuln;
};
/* Function */
/* End Functions */
/* Container filtering */

struct mnt_namespace {
    // This field was removed in https://github.com/torvalds/linux/commit/1a7b8969e664d6af328f00fe6eb7aabd61a71d13
    #if LINUX_VERSION_CODE < KERNEL_VERSION(5, 11, 0)
        atomic_t count;
    #endif
        struct ns_common ns;
};
/*
 * Create a buffer for sending event data to userspace
 */
BPF_PERF_OUTPUT(events);

static inline int _mntns_filter(unsigned int mntnsid) {
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
        return inum == mntnsid;
}

static inline int container_should_be_filtered(unsigned int mntnsid) {
        return _mntns_filter(mntnsid);
}

/* End Container filtering */


/*
 * Attach to the "fuse_copy_page" 
 */


int kprobe__fuse_copy_page(struct pt_regs *ctx, struct fuse_copy_state *cs, struct page **pagep,
			  unsigned offset, unsigned count, int zeroing) {
    if(!container_should_be_filtered(MOUNT_NS_ID))
        return 0;
    
    u64 gid_uid;
    u64 pid_tgid;
    struct data_t data = {};
    /*
     * Gather event data
     */
    gid_uid = bpf_get_current_uid_gid();
    pid_tgid = bpf_get_current_pid_tgid();

    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    data.uid = __LOWER(gid_uid);
    data.gid = __UPPER(gid_uid);
    data.pid = __UPPER(pid_tgid);
    data.is_vuln = 0;

    /* Tracing/Monitoring log */
    events.perf_submit(ctx, &data, sizeof(data));
    return 0;
}


