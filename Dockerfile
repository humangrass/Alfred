FROM python:3.11-slim

COPY src/ /app/

WORKDIR /app
RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "-u", "alfred.py"]
