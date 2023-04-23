FROM python:3.10
LABEL maintainer="Pawel Rzepecki <pawel.rzepecki21@gmail.com>"

COPY app /app
WORKDIR /app

RUN python3 -m venv /venv
RUN chmod +x venv/Scripts/activate
RUN venv/Scripts/activate
RUN pip install -r /app/requirements.txt

CMD python -m http.server & python app.py