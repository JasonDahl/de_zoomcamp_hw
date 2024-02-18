import io
import pandas as pd
import requests
import pyarrow as pa
import pyarrow.parquet as pq

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """

    months = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    root_url = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
    

        # Define data types for columns
    data_types = {
        'VendorID': pa.int64(),  # Using PyArrow data type for integers
        'lpep_pickup_datetime': pa.timestamp('ns'),  # Using PyArrow data type for timestamps
        'lpep_dropoff_datetime': pa.timestamp('ns'),
        'store_and_fwd_flag': pa.string(),  # Using PyArrow data type for strings
        'RatecodeID': pa.int64(),
        'PULocationID': pa.int64(),
        'DOLocationID': pa.int64(),
        'passenger_count': pa.int64(),
        'trip_distance': pa.float64(),  # Using PyArrow data type for floats
        'fare_amount': pa.float64(),
        'extra': pa.float64(),
        'mta_tax': pa.float64(),
        'tip_amount': pa.float64(),
        'tolls_amount': pa.float64(),
        'improvement_surcharge': pa.float64(),
        'total_amount': pa.float64(),
        'payment_type': pa.int64(),
        'trip_type': pa.int64(),
        'congestion_surcharge': pa.float64()
    }

    dfs=[]
    for month in months:
        filestring = f'green_tripdata_2022-{month:02d}.parquet'
        file_url = f'{root_url}/{filestring}'

        response = requests.get(file_url)
        # Create a file-like object from response content
        file_like_object = io.BytesIO(response.content)

        pa_table = pq.read_table(
            source=file_like_object,
            schema=pa.schema(data_types)
        )
        dfs.append(pa_table.to_pandas())
       
    print(dfs[-1].info())
    return pd.concat(dfs, ignore_index=True)

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
