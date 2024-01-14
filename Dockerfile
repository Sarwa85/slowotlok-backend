FROM python:3.10-slim-bookworm
COPY flaskr /app/flaskr
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV FLASK_APP=flaskr
CMD flask run --host 0.0.0.0 --port 9999
