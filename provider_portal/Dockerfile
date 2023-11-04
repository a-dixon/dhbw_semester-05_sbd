FROM python

WORKDIR /provider_portal

RUN apt update
RUN apt install python3-pip -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

ENV FLASK_ENV=development

CMD [ "python3", "run.py" ]