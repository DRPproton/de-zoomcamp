import requests
import os
# import pyarrow as pa
# import pyarrow.parquet as pq
# import pandas as pd
# import io



def download_taxi_data(year, service):
    
    root_path = os.getcwd()

    for i in range(12):

        # sets the month part of the file_name string
        month = '0' + str(i+1)
        month = month[-2:]

        # csv file_name
        # file_name = f"{service}_tripdata_{year}-{month}.parquet"
        file_name = f"{service}_tripdata_{year}-{month}.csv.gz"

        # Making download url
        request_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/{service}_tripdata_{year}-{month}.csv.gz'
        # request_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/{service}_tripdata_{year}-{month}.csv.gz'
        # request_url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{service}_tripdata_{year}-{month}.parquet'

        # Save the file in a dataframe
        r = requests.get(request_url)
        # data = io.BytesIO(r.content)
        # df = pq.read_table(data).to_pandas()
        if os.path.exists(f'{service}-{year}'):
            os.chdir(f'{service}-{year}')
        else:
            os.makedirs(f'{service}-{year}')
            os.chdir(f'{service}-{year}')

        # save the file locally
        open(file_name, 'wb').write(r.content)
        print(f"Local: {file_name}")

        os.chdir(root_path)

def download_fhv_taxi_data(year):
    
    root_path = os.getcwd()

    for i in range(12):

        # sets the month part of the file_name string
        month = '0' + str(i+1)
        month = month[-2:]

        # csv file_name
        file_name = f"fhv_tripdata_{year}-{month}.csv.gz"

        # Making download url
        # request_url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/fhv/fhv_tripdata_{year}-{month}.csv.gz'
        # request_url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/fhv_tripdata_{year}-{month}.parquet'
        # request_url = f'https://d37ci6vzurychx.cloudfront.net/trip-data/{service}_tripdata_{year}-{month}.parquet'

        # Save the file in a dataframe
        r = requests.get(request_url)
        # data = io.BytesIO(r.content)
        # df = pq.read_table(data).to_pandas()
        if os.path.exists(f'fhv-{year}'):
            os.chdir(f'fhv-{year}')
        else:
            os.makedirs(f'fhv-{year}')
            os.chdir(f'fhv-{year}')

        # save the file locally
        open(file_name, 'wb').write(r.content)
        print(f"Local: {file_name}")

        os.chdir(root_path)

# download_taxi_data('2019', 'yellow')
download_taxi_data('2020', 'yellow')
# download_taxi_data('2021', 'yellow')

# download_taxi_data('2019', 'green')
# download_taxi_data('2020', 'green')
# download_taxi_data('2021', 'green')
# download_taxi_data('2022', 'green')
        

# download_fhv_taxi_data(2019)