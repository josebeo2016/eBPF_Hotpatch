# Run this script to get the container shell
# then run the test binary file
gcc ptrace.c -o test
docker build -t ptrace-phucdt .
docker run --rm -it --security-opt apparmor=unconfined --name test ptrace-phucdt:latest bash