# Module 1: Docker, SQL, and Terraform

This project demonstrates hands-on experience with Docker, SQL, and Terraform, emphasizing practical skills in data handling, exploration, and infrastructure setup. It combines both local and cloud-based technologies.

Requirements:
- Docker
- Docker-Compose
- postgresql / pgcli
- Terraform
- Jupyter Notebook

## Project Development

### Part 1: Containerization with Docker and database administration with postgreSQL

#### Downloading the data

For this project we'll use NYC green taxi trips from September 2019.  While NYC Open Data now distributes these data as parquet files, we'll use archived CSV versions of the datafiles:
```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz
```
We also need the dataset with zones:
```bash
wget https://s3.amazonaws.com/nyc-tlc/misc/taxi+_zone_lookup.csv
```

To persist the data locally, we create a folder "data/ny_taxi_postgresql_data/" to use for volume mapping into the Docker container that will host our database. Then, we run the container with the following terminal command, which maps container port 5432 to localhost:5432:
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/data/ny_taxi_postgresql_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

#### Extract, Transform, Load (ETL)

We perform initial database development in a Jupyter [Notebook](https://github.com/JasonDahl/de_zoomcamp_hw/blob/main/dehw_01_docker_sql/DE_HW1_Docker_SQL_Terraform.ipynb, "View notebook").  We use SQL Alchemy to create a connection to localhost:5432, and use pandas to transform the data before loading it into a table in the container.  

####   Data ingestion

The ETL code in the notebook forms the basis of the ingestion script [ingest_data.py](https://github.com/JasonDahl/de_zoomcamp_hw/blob/main/dehw_01_docker_sql/ingest_data.py, "View script").  The script can be run locally:
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=green_taxi_trips \
  --url=${URL}
```

This script can be loaded into a Docker container using the included [Dockerfile](https://github.com/JasonDahl/de_zoomcamp_hw/blob/main/dehw_01_docker_sql/Dockerfile, "View Dockerfile") with the command
```bash
docker build -t taxi_ingest:v001 .
```

Linux may have a problem building it:
```bash
error checking context: 'can't stat '/home/name/data_engineering/ny_taxi_postgres_data''.
```
We solved it with ```.dockerignore```:

- Created a folder ```data```.
- Moved ```ny_taxi_postgresql_data``` to ```data``` (you might need to use sudo for that)
- Mapped ```-v $(pwd)/data/ny_taxi_postgresql_data:/var/lib/postgresql/data```
- Created a file ```.dockerignore``` and add ```data``` there

To run the script with Docker:
```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

#### Querying the database

We can query the database using PGAdmin, running on localhost:8080
To run Postgres and pgAdmin together, create a network:
```bash
docker network create pg-network
```
Run Postgres
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/data/ny_taxi_postgresql_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```
Run pgAdmin
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

We can also query the database using SQLAlchemy.  See several examples in the [Notebook](https://github.com/JasonDahl/de_zoomcamp_hw/blob/main/dehw_01_docker_sql/DE_HW1_Docker_SQL_Terraform.ipynb, "View notebook") .

#### Docker-Compose
We can use Docker-Compose to orchestrate the containers rather than starting the containers manually.  View the configuration in [docker-compose.yaml](https://github.com/JasonDahl/de_zoomcamp_hw/blob/main/dehw_01_docker_sql/docker-compose.yaml).

Run it with:
```bash
docker-compose up
```
Run in detached mode:
```bash
docker-compose up -d
```
Shutting it down:
```bash
docker-compose down
```

### Part 2: Resource provisioning with Terraform

Terraform allows us to create and destroy GCP resources as part of our workflow, allowing us to access Infrastructure as Code. Terraform requires a valid service account and credentials.  

Configuration is in [main.tf](https://github.com/JasonDahl/de_zoomcamp_hw/blob/main/dehw_01_docker_sql/main.tf) and environment variables are defined in [variables.tf](https://github.com/JasonDahl/de_zoomcamp_hw/blob/main/dehw_01_docker_sql/variables.tf)

Initialize terraform in a local folder with ```terraform init```.

Provision resources (in this case a GCS Bucket and a BigQuery resource) with:
```bash
terraform apply
```

Deprovision resources with:
```bash
terraform destroy
```

