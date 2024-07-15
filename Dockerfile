FROM python:3.11-slim-buster

WORKDIR /app

RUN pip install requests

COPY apiAlerts.py /app/

ENTRYPOINT ["python", "apiAlerts.py" ]
CMD ["python", "apiAlerts.py", "-h"]
