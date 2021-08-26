FROM python:3.7

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak \
    && sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
    && sed -i "s@security.debian.org/debian-security@mirrors.aliyun.com/debian-security@g" /etc/apt/sources.list \
    && cat /etc/apt/sources.list

RUN apt-get clean
RUN apt-get update && apt-get install gcc -y  && apt-get install build-essential python3-dev python3-mysqldb python-mysqldb python-dev -y && apt-get clean

RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /app/requirements.txt && rm -rf /root/.cache/pip

EXPOSE 8001

COPY . /app/