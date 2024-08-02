FROM ubuntu:latest
LABEL authors="egork"

ENTRYPOINT ["top", "-b"]