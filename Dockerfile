FROM python:3.12

COPY --from=ghcr.io/astral-sh/uv:0.11 /uv /usr/local/bin/uv

ENV UV_PROJECT_ENVIRONMENT=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY pyproject.toml uv.lock /tmp/deps/
RUN cd /tmp/deps && uv sync --frozen --no-dev

COPY ./ /app
WORKDIR /app

ENV PYTHONPATH=/app
ENV MODULE_NAME=wsgi
EXPOSE 80
ENTRYPOINT ["./entrypoint.sh"]
CMD ["./start.sh"]
