FROM python:slim
WORKDIR /django
ADD . /django
RUN pip install -r requirements.txt