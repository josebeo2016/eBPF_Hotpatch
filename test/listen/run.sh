# Run this script to get the container shell
# then run the test binary file
gcc listen.c -o test
docker build -t listen-phucdt .
docker run --rm -it --security-opt apparmor=unconfined --name test listen-phucdt:latest bash