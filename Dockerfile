FROM python:3.13-slim

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install gunicorn

RUN apt-get update && apt-get install -y curl wget && rm -rf /var/lib/apt/lists/*

COPY . .

EXPOSE 4175

CMD ["gunicorn", "--bind", "0.0.0.0:4175", "app:server"]
