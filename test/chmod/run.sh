gcc linux-chmod.c -o test-chmod
docker build -t chmod-songi .
docker run --rm -it --security-opt apparmor=unconfined --name test-chmod chmod-songi:latest bash