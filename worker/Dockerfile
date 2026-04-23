# -------- Stage 1: Build --------
FROM python:3.12-slim-bookworm AS builder

RUN apt-get update && apt-get upgrade -y && apt-get clean

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# -------- Stage 2: Runtime --------
FROM python:3.12-slim

WORKDIR /app

# Create non-root user
RUN addgroup --system appgroup && adduser --system --group appuser

# Copy dependencies
COPY --from=builder /install /usr/local

# Copy source code
COPY . .

RUN chown -R appuser:appgroup /app

USER appuser

# Healthcheck (checks Redis connectivity)
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s \
  CMD python -c "import redis, os; r=redis.Redis(host=os.getenv('REDIS_HOST','localhost'), port=6379); r.ping()" || exit 1

CMD ["python", "worker.py"]