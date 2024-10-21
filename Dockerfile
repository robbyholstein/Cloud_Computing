FROM alpine
RUN apk add --no-cache python3 py3-pip
COPY count_container.py /home/script/
WORKDIR /home/data
COPY IF.txt /home/data/
COPY AlwaysRememberUsThisWay.txt /home/data/
ENTRYPOINT [ "python3", "/home/script/count_container.py"]