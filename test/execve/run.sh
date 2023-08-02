gcc linux-execve.c -o test-execve
docker build -t execve-songi .
docker run --rm -it --security-opt apparmor=unconfined --name test-execve execve-songi:latest bash