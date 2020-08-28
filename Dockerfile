FROM python:3.8.2
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install build-essential openssl libssl-dev swig python3-dev -y
RUN mkdir /opt/myproj
WORKDIR /opt/myproj/

COPY ./ /opt/myproj/
RUN pip install --upgrade pip
RUN pip install -r requires/base.pip

COPY ./docker-entrypoint.sh /
RUN chmod +x /docker-entrypoint.sh
ENTRYPOINT ["/docker-entrypoint.sh"]
