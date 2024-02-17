from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path

import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from pyarrow.fs import GcsFileSystem

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_from_google_cloud_storage(*args, **kwargs):
    """
    Template for loading data from a Google Cloud Storage bucket.
    Specify your configuration settings in 'io_config.yaml'.

    Docs: https://docs.mage.ai/design/data-loading#googlecloudstorage
    """

    bucket_name = 'mage-zoomcamp-jason-dahl-1'
    blob_prefix = 'green_taxi_data/'
    root_path = f'{bucket_name}/{blob_prefix}'

    # Define data types for columns
    data_types = {
        'vendor_id': pa.int64(),  # Using PyArrow data type for integers
        'lpep_pickup_datetime': pa.timestamp('s'),  # Using PyArrow data type for timestamps
        'lpep_dropoff_datetime': pa.timestamp('s'),
        'passenger_count': pa.int64(),
        'trip_distance': pa.float64(),  # Using PyArrow data type for floats
        'ratecode_id': pa.int64(),
        'store_and_fwd_flag': pa.string(),  # Using PyArrow data type for strings
        'pu_location_id': pa.int64(),
        'do_location_id': pa.int64(),
        'payment_type': pa.int64(),
        'fare_amount': pa.float64(),
        'extra': pa.float64(),
        'mta_tax': pa.float64(),
        'tip_amount': pa.float64(),
        'tolls_amount': pa.float64(),
        'improvement_surcharge': pa.float64(),
        'total_amount': pa.float64(),
        'congestion_surcharge': pa.float64(),
        'lpep_pickup_date': pa.timestamp('s')
    }

    pa_table = pq.read_table(
        source=root_path,
        schema=pa.schema(data_types),
        filesystem=GcsFileSystem()
    )
    return pa_table.to_pandas()
   

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'