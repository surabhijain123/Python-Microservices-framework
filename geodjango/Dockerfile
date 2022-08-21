FROM python:3.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
RUN apt-get update \
    && apt-get -y install netcat gcc postgresql \
    && apt-get clean
RUN apt-get update \
    && apt-get install -y binutils libproj-dev gdal-bin python3-gdal
COPY requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt
COPY . /app
