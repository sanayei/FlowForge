FROM public.ecr.aws/ubuntu/ubuntu:22.04

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /tmp/
RUN pip3 install --no-cache-dir -r /tmp/requirements.txt

WORKDIR /app
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["python3"]