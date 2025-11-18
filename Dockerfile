FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y

RUN pip install -r requirements.txt

EXPOSE 10000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]