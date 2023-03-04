FROM python:3.10

WORKDIR /app
COPY . /app

RUN apt-get update && apt-get install -y ffmpeg
RUN git pull

RUN python -m pip install \
--upgrade pip \
--upgrade setuptools \
-r requirements.txt

CMD ["python", "aicy.py"]
