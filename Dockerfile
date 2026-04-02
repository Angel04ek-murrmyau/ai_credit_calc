FROM python:3.14.3-slim-trixie
ARG GIGACHAT_CRED_ARG
ENV GIGACHAT_CREDENTIALS=$GIGACHAT_CRED_ARG
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8
WORKDIR /app
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages
COPY . .
CMD ["python", "run.py"]