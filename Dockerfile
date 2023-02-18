FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y ffmpeg

RUN python -m pip install \
--upgrade pip \
--upgrade setuptools \
-r requirements.txt

CMD ["python3.10", "entrancebot.py"]