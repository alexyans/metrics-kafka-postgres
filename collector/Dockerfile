FROM python:3.6

ADD . /collector
WORKDIR /collector
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

HEALTHCHECK CMD bash scripts/healthcheck.sh

CMD ["/bin/bash", "scripts/run.sh"]
