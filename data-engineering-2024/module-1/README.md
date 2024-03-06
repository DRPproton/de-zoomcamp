## Commands 

Downloading the data

```bash
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz 
```

### Running Postgres with Docker

#### Windows

Running Postgres on Windows (note the full path)

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /c/Users/dashi/Documents/dezoomcamp/data-engineering-2024/module-1/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```


#### Linux and MacOS


```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v $(pwd)/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

If you see that `ny_taxi_postgres_data` is empty after running
the container, try these:

* Deleting the folder and running Docker again (Docker will re-create the folder)
* Adjust the permissions of the folder by running `sudo chmod a+rwx ny_taxi_postgres_data`


### CLI for Postgres

Installing `pgcli`

```bash
pip install pgcli
```

If you have problems installing `pgcli` with the command above, try this:

```bash
conda install -c conda-forge pgcli
pip install -U mycli
```

Using `pgcli` to connect to Postgres

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

### pgAdmin

Running pgAdmin

```bash
docker run -it --rm \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

### Running Postgres and pgAdmin together

Create a network

```bash
docker network create pg-network
```

Run Postgres (change the path)

```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v /c/Users/dashi/Documents/dezoomcamp/data-engineering-2024/module-1/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:13
```

Run pgAdmin

```bash
docker run -it --rm \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

### Data ingestion

Running locally

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --table_name=yellow_taxi_trips \
  --url=${URL}
```

Build the image

```bash
docker build -t taxi_ingest:v001 .
```

On Linux you may have a problem building it:

```
error checking context: 'can't stat '/home/name/data_engineering/ny_taxi_postgres_data''.
```

You can solve it with `.dockerignore`:

* Create a folder `data`
* Move `ny_taxi_postgres_data` to `data` (you might need to use `sudo` for that)
* Map `-v $(pwd)/data/ny_taxi_postgres_data:/var/lib/postgresql/data`
* Create a file `.dockerignore` and add `data` there
* Check [this video](https://www.youtube.com/watch?v=tOr4hTsHOzU&list=PL3MmuxUbc_hJed7dXYoJw8DoCuVHhGEQb) (the middle) for more details 


Run the script with Docker

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it --rm \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pgdatabase \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}
```

### Docker-Compose 

Run it:

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

Note: to make pgAdmin configuration persistent, create a folder `data_pgadmin`. Change its permission via

```bash
sudo chown 5050:5050 data_pgadmin
```

and mount it to the `/var/lib/pgadmin` folder:

```yaml
services:
  pgadmin:
    image: dpage/pgadmin4
    volumes:
      - ./data_pgadmin:/var/lib/pgadmin
    ...
```


```

Docker - Could not change permissions of directory "/var/lib/postgresql/data": Operation not permitted 
$ docker run -it\
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="admin" \
  -e POSTGRES_DB="ny_taxi" \
  -v "/mnt/path/to/ny_taxi_postgres_data":"/var/lib/postgresql/data" \
  -p 5432:5432 \
  postgres:13

CCW
The files belonging to this database system will be owned by user "postgres".
This use The database cluster will be initialized with locale "en_US.utf8".
The default databerrorase encoding has accordingly been set to "UTF8".
xt search configuration will be set to "english".

Data page checksums are disabled.
fixing permissions on existing directory /var/lib/postgresql/data ... initdb: 
error: could not change permissions of directory "/var/lib/postgresql/data": Operation not permitted  volume
One way to solve this issue is to create a local docker volume and map it to postgres data directory /var/lib/postgresql/data
The input dtc_postgres_volume_local must match in both commands below

$ docker volume create --name dtc_postgres_volume_local -d local
$ docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v dtc_postgres_volume_local:/var/lib/postgresql/data \
  -p 5432:5432\
  postgres:13

To verify the above command works in (WSL2 Ubuntu 22.04, verified 2024-Jan), go to the Docker Desktop app and look under Volumes - dtc_postgres_volume_local would be listed there. The folder ny_taxi_postgres_data would however be empty, since we used an alternative config.
```
