FROM python:3.8
WORKDIR /app
COPY ./alert-bot/requirements.txt .
RUN pip3 install -r requirements.txt
COPY ./alert-bot .
CMD ["python3", "main.py"]
