FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements.txt

COPY . .
COPY static /app/static

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]