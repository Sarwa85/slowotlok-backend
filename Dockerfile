FROM arm64v8/python:3.10-slim-bookworm
LABEL org.opencontainers.image.source=https://github.com/Sarwa85/slowotlok-backend-flask
LABEL org.opencontainers.image.description="slowotlok-backend"
LABEL org.opencontainers.image.licenses=MIT
COPY flaskr /app/flaskr
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ENV FLASK_APP=flaskr
CMD flask run --host 0.0.0.0 --port 9999
