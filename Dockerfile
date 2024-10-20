FROM python:3.12

COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip
RUN pip install --upgrade wheel
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY ./ /app
WORKDIR /app

ENV PYTHONPATH=/app
ENV MODULE_NAME=wsgi
EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]
CMD ["./start.sh"]
