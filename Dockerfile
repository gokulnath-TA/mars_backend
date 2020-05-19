FROM python:3.6
RUN apt-get update && apt-get install -y python3-pip python3-setuptools python3-dev libcurl4-openssl-dev libssl-dev
RUN apt-get install curl
RUN apt-get install apt-transport-https
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/ubuntu/16.04/prod.list | tee /etc/apt/sources.list.d/msprod.list
RUN apt-get update
ENV ACCEPT_EULA=y DEBIAN_FRONTEND=noninteractive
RUN apt-get install mssql-tools unixodbc-dev -y
RUN pip3 install pyodbc
RUN pip3 install --upgrade pip
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
COPY . /app/
WORKDIR /app
COPY requirement.txt /app/
RUN pip3 install -r requirement.txt
EXPOSE 8000
ENTRYPOINT python3 manage.py runserver 0.0.0.0:8000