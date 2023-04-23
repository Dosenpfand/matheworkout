FROM python:3.11-bullseye

RUN apt-get update
RUN apt-get -y install postgresql sudo

COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./app /app
WORKDIR /app/

ENV PYTHONPATH=/app

EXPOSE 8080

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]
