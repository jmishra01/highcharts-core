"""Unit tests for ``highcharts/utility_functions``"""

import pytest
from abc import ABC, abstractmethod

import numpy as np
from validator_collection import checkers

from highcharts_core import utility_functions, constants


@pytest.mark.parametrize('kwargs, expected_column_names, expected_records, error', [
    ({
        'csv_data': "Date,Header\r\n01/01/2023,2\r\n01/02/2023,4\r\n01/03/2023,8"
     }, ['Date', 'HeadCount'], 3, None),
])
def test_parse_csv(kwargs, expected_column_names, expected_records, error):
    if not error:
        columns, records_as_dicts = utility_functions.parse_csv(**kwargs)
        assert columns is not None
        assert len(columns) == len(expected_column_names)
        
        assert records_as_dicts is not None
        assert len(records_as_dicts) == expected_records
    else:
        with pytest.raises(error):
            result = utility_functions.parse_csv(**kwargs)
            

@pytest.mark.parametrize('camelCase, expected, error', [
    ('camelCase', 'camel_case', None),
    ('camelCaseURL', 'camel_case_url', None),
    ('camel123Case', 'camel123_case', None),
])
def test_to_snake_case(camelCase, expected, error):
    if not error:
        result = utility_functions.to_snake_case(camelCase)
        assert result == expected
    else:
        with pytest.raises(error):
            result = utility_functions.to_snake_case(camelCase)


@pytest.mark.parametrize('value, expected_dtype, error', [
    ([1, 2, 3], np.int32, None),
    ([43934, np.nan, 65165, 81827, 112143, 142383, 171533, 165174, 155157, 161454, 154610], np.float64, None),
    ([{'test': 123}, {'test': 456}], np.dtype('O'), None),

])
def test_to_ndarray(value, expected_dtype, error):
    if not error:
        result = utility_functions.to_ndarray(value)
        assert isinstance(result, np.ndarray)
        assert result.shape[0] == len(value)
        assert result.dtype == expected_dtype
    else:
        with pytest.raises(error):
            result = utility_functions.to_ndarray(value)
            

@pytest.mark.parametrize('as_ndarray, force_enforced_null, error', [
    (np.asarray([1, 2, 3]), False, None),
    (np.asarray([43934, np.nan, 65165, 81827, 112143, 142383, 171533, 165174, 155157, 161454, 154610]), False, None),
    (np.asarray([{'test': 123}, {'test': 456}]), False, None),
    (np.asarray([1, 2, np.nan, 4, 5, 6]), False, None),

    (np.asarray([1, 2, 3]), True, None),
    (np.asarray([43934, np.nan, 65165, 81827, 112143, 142383, 171533, 165174, 155157, 161454, 154610]), True, None),
    (np.asarray([{'test': 123}, {'test': 456}]), True, None),
    (np.asarray([1, 2, np.nan, 4, 5, 6]), True, None),
])
def test_from_ndarray(as_ndarray, force_enforced_null, error):
    if not error:
        print(as_ndarray.dtype)
        result = utility_functions.from_ndarray(as_ndarray, 
                                                force_enforced_null = force_enforced_null)
        assert isinstance(result, list)
        assert len(result) == as_ndarray.shape[0]
        for item in result:
            if checkers.is_numeric(item):
                continue
            if isinstance(item, dict):
                continue
            if force_enforced_null:
                assert isinstance(item, constants.EnforcedNullType)
            else:
                assert item is None