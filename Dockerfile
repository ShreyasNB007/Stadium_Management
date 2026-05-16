FROM python:3.11

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 5000

COPY wait-for-db.sh /wait-for-db.sh

RUN chmod +x /wait-for-db.sh

CMD ["/wait-for-db.sh"]