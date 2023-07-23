import pandas as pd
import pytest

from data_quality_reports.dqr import DQR


@pytest.fixture
def df():
    file_path = "./tests/fixtures/demo_data.csv"
    return pd.read_csv(file_path, sep=",", header=0)


@pytest.fixture
def dqr(df):
    return DQR(df)


@pytest.fixture
def data_types_df():
    file_path = "./tests/fixtures/data_types_test.csv"
    return pd.read_csv(file_path, sep=",", header=0)


@pytest.fixture
def create_continuous_df():
    file_path = "./tests/fixtures/_continuous_df_test.csv"
    return pd.read_csv(file_path, sep=",", header=0)


@pytest.fixture
def create_categorical_df():
    file_path = "./tests/fixtures/_categorical_df_test.csv"
    return pd.read_csv(file_path, sep=",", header=0)


@pytest.fixture
def update_continuous_df():
    file_path = "./tests/fixtures/_update_continuous_df_test.csv"
    return pd.read_csv(file_path, sep=",", header=0)


@pytest.fixture
def update_categorical_df():
    file_path = "./tests/fixtures/_update_categorical_df_test.csv"
    return pd.read_csv(file_path, sep=",", header=0)


@pytest.fixture
def continuous_df():
    file_path = "./tests/fixtures/continuous_data.csv"
    return pd.read_csv(file_path, sep=",", header=0, index_col=0)


@pytest.fixture
def categorical_df():
    file_path = "./tests/fixtures/categorical_data.csv"
    return pd.read_csv(file_path, sep=",", header=0, index_col=0)


@pytest.fixture()
def temp_dir(tmpdir_factory):
    return str(tmpdir_factory.mktemp("tests"))


@pytest.fixture
def categorical_data_path(temp_dir):
    return f"{temp_dir}/categorical_data.csv"


@pytest.fixture
def continuous_data_path(temp_dir):
    return f"{temp_dir}/continuous_data.csv"


def test_get_data_types(dqr, data_types_df):
    data_types = dqr._get_data_types()
    pd.testing.assert_frame_equal(data_types, data_types_df)


def test_create_continuous_df(dqr, create_continuous_df):
    continuous_df = dqr._create_continuous_df()
    pd.testing.assert_frame_equal(continuous_df, create_continuous_df)


def test_create_categorical_df(dqr, create_categorical_df):
    categorical_df = dqr._create_categorical_df()
    pd.testing.assert_frame_equal(categorical_df, create_categorical_df)


def test_update_continuous_df(dqr, update_continuous_df):
    continuous_df = dqr._create_continuous_df()
    updated_df = dqr._update_continuous_df(continuous_df)
    pd.testing.assert_frame_equal(updated_df, update_continuous_df)


def test_update_categorical_df(dqr, update_categorical_df):
    categorical_df = dqr._create_categorical_df()
    updated_df = dqr._update_categorical_df(categorical_df)
    pd.testing.assert_frame_equal(updated_df, update_categorical_df)


def test_get_continuous_df(dqr, continuous_df):
    assert dqr.get_continuous_df().equals(continuous_df)


def test_get_categorical_df(dqr, categorical_df):
    assert dqr.get_categorical_df().equals(categorical_df)


def test_write_continuous_to_csv(dqr, continuous_df, categorical_data_path, continuous_data_path):
    dqr.write_to_csv(continuous_data_path, categorical_data_path)
    loaded_continuous_df = pd.read_csv(continuous_data_path, sep=",", header=0, index_col=0)
    pd.testing.assert_frame_equal(loaded_continuous_df, continuous_df)


def test_write_categorical_to_csv(dqr, categorical_df, categorical_data_path, continuous_data_path):
    dqr.write_to_csv(continuous_data_path, categorical_data_path)
    loaded_categorical_df = pd.read_csv(categorical_data_path, sep=",", header=0, index_col=0)
    pd.testing.assert_frame_equal(loaded_categorical_df, categorical_df)
