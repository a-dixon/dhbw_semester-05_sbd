FROM python

WORKDIR /smart_meter

RUN apt update
RUN apt install python3-pip -y

EXPOSE 5000

COPY . .

ENV FLASK_ENV=development

