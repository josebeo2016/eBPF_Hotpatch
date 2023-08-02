gcc connect.c -o test
docker build -t connect-phucdt .
docker run --rm -it --security-opt apparmor=unconfined --name test connect-phucdt:latest bash