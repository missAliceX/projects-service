FROM python:3.9.6

WORKDIR /app
COPY main.py main.py
COPY requirements.txt .
COPY src src

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python3", "main.py" ]