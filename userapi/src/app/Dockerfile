# ---- Stage 1: Build ----
FROM python:3.11-slim AS build

# Set working directory
WORKDIR /app

# Copy requirements first for caching
COPY requirements.txt .

# Install build dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# ---- Stage 2: Run ----
FROM python:3.11-slim

WORKDIR /app

# Copy installed packages from build stage
COPY --from=build /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=build /usr/local/bin /usr/local/bin

# Copy app source code
COPY . .

# Expose port
EXPOSE 8000

# Default command
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
