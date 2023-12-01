FROM python

WORKDIR /app/provider_portal

RUN apt update
RUN apt install python3-pip -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

ENV FLASK_ENV=development
ENV PYTHONWARNINGS="ignore:Unverified HTTPS request"

CMD [ "python3", "run.py" ]