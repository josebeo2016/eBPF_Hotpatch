# Run this script to get the container shell
# then run the test binary file
gcc ptrace_attach.c -o test
gcc dummy.c -o dummy
docker build -t ptrace_attach-phucdt .
docker run --rm -it --security-opt apparmor=unconfined --name test ptrace_attach-phucdt:latest bash