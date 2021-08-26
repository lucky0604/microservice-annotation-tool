FROM python:3.8

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak \
    && sed -i "s@http://deb.debian.org@http://mirrors.aliyun.com@g" /etc/apt/sources.list \
    && sed -i "s@security.debian.org/debian-security@mirrors.aliyun.com/debian-security@g" /etc/apt/sources.list \
    && cat /etc/apt/sources.list

RUN apt-get update
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'python3-dev' \
    'pkg-config' \
    'libavformat-dev' \
    'libavcodec-dev' \
    'libavdevice-dev' \
    'libavutil-dev' \
    'libswscale-dev' \
    'libavresample-dev' \
    'libxext6'  -y


RUN pip install -i https://mirrors.aliyun.com/pypi/simple/ -r /app/requirements.txt && rm -rf /root/.cache/pip

EXPOSE 8002

COPY . /app/
