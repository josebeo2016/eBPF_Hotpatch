gcc linux-clone.c -o test-clone
docker build -t clone-songi .
docker run --rm -it --security-opt apparmor=unconfined --name test-clone clone-songi:latest bash