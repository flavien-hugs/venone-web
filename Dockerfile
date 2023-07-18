FROM python:3.10

RUN echo "vm.overcommit_memory = 1" >> /etc/sysctl.conf

RUN apt-get update && apt-get install -y sysfsutils

WORKDIR /venone

COPY ./env/local.txt /venone/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    VIRTUAL_ENV=/venv \
    PATH=/venv/bin:$PATH

RUN python -m venv $VIRTUAL_ENV && \
    pip install --upgrade pip && \
    pip install -r local.txt

COPY . /venone

RUN chgrp -R 0 /venone && \
    chmod -R g+rwX /venone

CMD ["python3", "runserver.py"]
