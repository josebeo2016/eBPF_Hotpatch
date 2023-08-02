gcc linux-setreuid.c -o test-setreuid
docker build -t setreuid-songi .
docker run --rm -it --security-opt apparmor=unconfined --name test-setreuid setreuid-songi:latest bash