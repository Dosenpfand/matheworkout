FROM python:3.9

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade wheel
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

COPY ./ /app

ENV PYTHONPATH=/app

EXPOSE 80

ENTRYPOINT ["/entrypoint.sh"]

CMD ["/start.sh"]
