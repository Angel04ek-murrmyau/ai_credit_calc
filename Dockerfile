FROM python:3.14.3-slim-trixie
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "run.py"]