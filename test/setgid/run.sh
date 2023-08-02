gcc linux-setgid.c -o test-setgid
docker build -t setgid-songi .
docker run --rm -it --security-opt apparmor=unconfined --name test-setgid setgid-songi:latest bash