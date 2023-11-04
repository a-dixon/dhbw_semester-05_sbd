FROM python

WORKDIR /smart_meter

RUN apt update
RUN apt install python3-pip -y

COPY . .

ENV FLASK_ENV=development

