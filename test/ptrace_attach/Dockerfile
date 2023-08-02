FROM ubuntu:latest
RUN apt update
RUN apt install curl netcat -y
ADD test /root/test
ADD dummy /root/dummy
WORKDIR /root/