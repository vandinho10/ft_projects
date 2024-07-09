# system base
FROM python:3-alpine

# define timezone
ENV TZ=America/Campo_Grande
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

# define workdir
WORKDIR /app

# update pip if outdated
RUN python -m pip install --upgrade pip

# import file requirements.txt
COPY ./requirements.txt requirements.txt

# install requirements from file
RUN pip install -r requirements.txt

# expose port
EXPOSE 5000

# define env
ENV FLASK_APP=app.py

CMD ["flask", "run", "--host=0.0.0.0"]
