gcc server.c -o server
gcc client.c -o client
docker build -t bind-phucdt .
docker run --rm -it --security-opt apparmor=unconfined --name test bind-phucdt:latest bash