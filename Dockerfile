FROM python:3.11-slim AS builder

# Install build dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    cmake \
    pkg-config \
    libglib2.0-dev \
    libfreetype6-dev \
    libpng-dev \
    libjpeg-dev \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim AS production

# Create non-root user
RUN groupadd -g 1000 homecv && \
    useradd -u 1000 -g homecv -s /bin/bash -m homecv

# Install only runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libglib2.0-0 \
    libfreetype6 \
    libpng16-16 \
    libjpeg62-turbo \
    libopenblas0 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy Python packages from builder stage
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=homecv:homecv . .

# Switch to non-root user
USER homecv

EXPOSE 9000

CMD ["gunicorn", "--bind", "0.0.0.0:9000", "--workers", "2", "run:app"]
