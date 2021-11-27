FROM python:3.8
WORKDIR /app
COPY ./alert-bot .
RUN pip3 install -r requirements.txt
ENV DVMN_TOKEN=123
ENV TELEGRAM_TOKEN=123
ENV CHAT_ID=123
CMD ["python3", "main.py"]
