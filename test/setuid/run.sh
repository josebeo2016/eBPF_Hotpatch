gcc linux-setuid.c -o test-setuid
docker build -t setuid-songi .
docker run --rm -it --security-opt apparmor=unconfined --name test-setuid setuid-songi:latest bash