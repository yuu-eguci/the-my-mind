FROM python:3.14-slim

WORKDIR /app

COPY requirements.txt requirements-dev.txt ./
RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

EXPOSE 8000
CMD ["flask", "--app", "local_test", "run", "--host", "0.0.0.0", "--port", "8000"]
