FROM python:3.11
RUN ln -sf /usr/share/zoneinfo/Asia/Tokyo /etc/localtime
RUN echo "Asia/Tokyo" > /etc/timezone

COPY . /app
COPY .env /app/.env
WORKDIR /app
RUN export $(cat .env | xargs)
RUN pip install --upgrade pip
RUN pip install -r requirements/production.txt

RUN apt-get clean
RUN apt-get install -y openssl

EXPOSE 5000

CMD ["/bin/bash", "app/bin/startup.sh"]
