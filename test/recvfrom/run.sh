gcc server.c -o server
gcc client.c -o client
docker build -t recvfrom-phucdt .
docker run --rm -it --security-opt apparmor=unconfined --name test recvfrom-phucdt:latest bash