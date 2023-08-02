# Run this script to get the container shell
# then run the test binary file
gcc accept.c -o test
docker build -t accept-phucdt .
docker run --rm -it --security-opt apparmor=unconfined --name test accept-phucdt:latest bash