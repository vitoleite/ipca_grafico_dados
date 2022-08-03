import pytest
from ipca.source.transform import dataFormat


def test_df_columns_gt_1():
    assert len(dataFormat().dataTransform().columns) > 1

def test_df_shape_gt_0():
    assert dataFormat().dataTransform().shape[0] > 0