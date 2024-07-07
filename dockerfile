FROM python:3.9-slim

ENV TZ=America/Campo_Grande
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

WORKDIR /app

COPY ./requirements.txt requirements.txt
RUN python -m pip install --upgrade pip && pip install -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
