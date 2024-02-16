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
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    
    # Convert CamelCase column names to snake_case
    data.rename(columns={'VendorID': 'vendor_id', 'RatecodeID': 'ratecode_id', 'PULocationID': 'pu_location_id', 'DOLocationID': 'do_location_id'}, inplace=True)
    
    # Remove missing passenger_count and trip_distance
    rows = len(data)
    print(f'Preprocessing {rows} rows')
    print('Preprocessing: rows with missing passenger_count:', data['passenger_count'].isnull().sum())
    print('Preprocessing: rows with zero passenger_count:', data['passenger_count'].isin([0]).sum())
    print('Preprocessing: rows with missing trip_distance:', data['trip_distance'].isnull().sum())
    print('Preprocessing: rows with zero trip_distance:', data['trip_distance'].isin([0]).sum())
    
    return data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    
@test
def test_zero_passengers(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rows with zero passengers'

@test
def test_missing_passengers(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['passenger_count'].isnull().sum() == 0, 'There are rows with zero passengers'

@test
def test_zero_trip_distance(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are rows with zero passengers'

@test
def test_missing_trip_distance(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output['trip_distance'].isnull().sum() == 0, 'There are rows with zero passengers'

@test
def test_vendors_id(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert 'vendor_id' in output.columns, 'The vendor_id column is missing'