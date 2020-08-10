#FROM python:3.6
#Based on python 3.7
FROM jjanzic/docker-python3-opencv   

WORKDIR /usr/app

ADD ./requirements.txt ./
RUN pip install -r requirements.txt
ADD ./ ./

CMD ["python3", "app.py"]
