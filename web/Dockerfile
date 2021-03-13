FROM debian

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
    && localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y build-essential libssl-dev libffi-dev python-dev python3-dev
RUN apt-get update && apt-get install -y python3-pip

RUN pip3 install --upgrade pip

COPY app/requirements.txt .

RUN pip3 install -r requirements.txt

ADD ./app .
COPY local_settings.py ./photobook/
#ADD  db.sqlite3 .
