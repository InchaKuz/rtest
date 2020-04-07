FROM python:3.7

COPY requirements.txt /opt/app/rtest/requirements.txt
WORKDIR /opt/app/rtest
RUN pip install -r requirements.txt
COPY . /opt/app/rtest/

ENTRYPOINT pytest
