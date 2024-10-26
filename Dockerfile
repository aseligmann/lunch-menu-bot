FROM python:3.12-slim

RUN apt-get update \
    && apt-get install -yq --no-install-recommends \
    python3.12 \
    python3-pip \
    python3-venv \
    && apt-get clean


WORKDIR /app

COPY . /app

ENV VIRTUAL_ENV="/app/venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN python3 -m venv $VIRTUAL_ENV --system-site-packages && \
    python -m pip install uv && \
    python -m uv pip install -r requirements.lock

ENV PYTHONUNBUFFERED=1

ENV PYTHONPATH=/app/src

CMD ["python3", "src/lunch_menu_bot/main.py"]
