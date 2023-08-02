```shell
sudo apt-get install bpfcc-tools linux-headers-$(uname -r)
```

## Source tree:

/bpf: c code
/libs: python code
/rules: example policy files
main.py: front-end
bpf.py: back-end

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
  