FROM python

WORKDIR /app/smart_meter

RUN apt update
RUN apt install python3-pip -y
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD [ "python3", "run.py" ]