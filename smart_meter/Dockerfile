FROM python

WORKDIR /smart_meter

RUN apt update
RUN apt install python3-pip -y
COPY ../requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

EXPOSE 5000

COPY . .

ENV FLASK_ENV=development

