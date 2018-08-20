FROM python:3.6

WORKDIR /usr/src/app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN useradd -ms /bin/bash relevanc
USER relevanc

EXPOSE 4000

ENTRYPOINT ["python","app.py"]