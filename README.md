```shell
sudo apt-get install bpfcc-tools linux-headers-$(uname -r)
```

## Source tree:

- /bpf: c code
- /libs: python code
- /rules: example policy files
- main.py: front-end
- bpf.py: back-end

## Usage:

```
python3 main.py -h
usage: main.py [-h] [-V] [-d] [-L LOG_FILE] [-p PID] [-N NAMESPACE] [--dockerid DOCKERID]
               --hook HOOK

Kubernetes dynamic eBPF policy security

optional arguments:
  -h, --help            show this help message and exit
  -V, --version         Show version
  -d, --debug           Enable debug log
  -L LOG_FILE, --log-file LOG_FILE
                        save log to file
  -p PID, --pid PID     container pid
  -N NAMESPACE, --namespace NAMESPACE
                        Mount namespace ID follow the reference:
                        bcc/docs/special_filtering.md
  --dockerid DOCKERID   Docker container ID to apply rule
  --hook HOOK           LSM probe to be used to hook eBPF program
  ```
  
## Demo eBPF Hotpatch for CVE-2022-0492

- Deploy vulnerable container:
```
cd test/cve-2022-0492
docker build -t test .
docker run --name test -it --cap-add=SYS_ADMIN --security-opt apparmor=unconfined --rm test:latest bash
```
- Inside the container, run exploit script

```
./exploit.sh "cat /etc/passwd"
```

- Open other terminal and apply patch
```
python3 src/main.py -d --dockerid test -f src/rules/cgroup_release_agent_write.yml
```

## Develop patch:
- Analyse original patching code
- Write eBPF program and store at `src/bpf/`
- Write rule yaml file and store at `src/rules/`

Follow the example bpf program at `src/bpf/cgroup_release_agent_write.c`