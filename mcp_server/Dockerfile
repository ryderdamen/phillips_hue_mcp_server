FROM python:3.11-slim

WORKDIR /app/src

COPY src/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ ./

EXPOSE 8000

CMD ["python", "main.py"]
