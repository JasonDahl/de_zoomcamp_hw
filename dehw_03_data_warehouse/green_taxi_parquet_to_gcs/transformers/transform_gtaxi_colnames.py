import pandas as pd

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    
    # Add a column for pickup date
    data['lpep_pickup_month'] = data['lpep_pickup_datetime'].dt.month
    
    # Convert CamelCase column names to snake_case
    data.rename(columns={
                        'VendorID': 'vendor_id',
                        'RatecodeID': 'ratecode_id',
                        'PULocationID': 'pu_location_id',
                        'DOLocationID': 'do_location_id'
                        }, 
                inplace=True)

    return data


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
