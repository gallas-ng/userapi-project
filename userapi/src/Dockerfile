# ---- Stage 1: Build ----
FROM python:3.11-slim AS build

WORKDIR /app

COPY app/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ---- Stage 2: Run ----
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy app folder
COPY app /app/app

ENV PYTHONPATH=/app
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
