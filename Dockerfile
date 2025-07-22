FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /code


# Install system dependencies for psycopg2 and GeoAlchemy2
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file into the container and install them
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Run the app by default
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
