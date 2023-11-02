FROM python:3.11
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN echo "Asia/Tokyo" > /etc/timezone
COPY backend /code
COPY .env /code/.env
WORKDIR /code
RUN export $(cat .env | xargs)
RUN pip install --upgrade pip
RUN pip install -r requirements/production.txt

RUN apt-get clean
RUN apt-get update -qqy && apt-get install -y netcat

EXPOSE 5000

CMD ["/bin/bash", "docker/startup.sh"]