FROM python:3.11-slim

WORKDIR /app

# Install OS dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install python packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Default command
CMD ["bash", "run.sh"]
