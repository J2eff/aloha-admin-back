FROM python:3.8.13-alpine3.14

COPY . .

RUN pip3 install -r requirements.txt
EXPOSE 4321
CMD python3 main.py