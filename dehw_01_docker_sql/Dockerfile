FROM python:3.9.1

# Install wget
RUN apt-get update && apt-get install -y wget

# Install dependencies
RUN pip install pandas sqlalchemy psycopg2-binary

WORKDIR /app

# Copy the required files
COPY ingest_data.py .
COPY ny_taxi_postgresql_data ny_taxi_postgresql_data

# Set the entry point
ENTRYPOINT ["python", "ingest_data.py"]