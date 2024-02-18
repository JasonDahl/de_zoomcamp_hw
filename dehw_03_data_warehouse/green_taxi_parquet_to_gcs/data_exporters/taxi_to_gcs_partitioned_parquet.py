import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow.fs import GcsFileSystem
import os

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

os.environ['GOOGLE_APPLICATION_CREDENTIALS']= "/home/src/airy-cortex-409620-b92a5cd53048.json"

bucket_name = 'mage-zoomcamp-jason-dahl-1'
project_id = 'airy-cortex-409620'

table_name = 'green_taxi_2022_pq'

root_path = f'{bucket_name}/{table_name}'

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    
    schema = pa.schema([
        ('vendor_id', pa.int64()),
        ('lpep_pickup_datetime', pa.timestamp('ns')),
        ('lpep_dropoff_datetime', pa.timestamp('ns')),
        ('store_and_fwd_flag', pa.string()),
        ('ratecode_id', pa.int64()),
        ('pu_location_id', pa.int64()),
        ('do_location_id', pa.int64()),
        ('passenger_count', pa.int64()),
        ('trip_distance', pa.float64()),
        ('fare_amount', pa.float64()),
        ('extra', pa.float64()),
        ('mta_tax', pa.float64()),
        ('tip_amount', pa.float64()),
        ('tolls_amount', pa.float64()),
        ('improvement_surcharge', pa.float64()),
        ('total_amount', pa.float64()),
        ('payment_type', pa.int64()),
        ('trip_type', pa.int64()),
        ('congestion_surcharge', pa.float64()),
        ('lpep_pickup_month', pa.int64())
    ])
    
    table = pa.Table.from_pandas(data, schema=schema)

    gcs = pa.fs.GcsFileSystem()

    pq.write_to_dataset(
        table,
        root_path = root_path,
        partition_cols = ['lpep_pickup_month'],
        filesystem = gcs
    )
