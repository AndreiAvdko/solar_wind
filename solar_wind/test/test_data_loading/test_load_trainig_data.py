from solar_wind.load_trainig_data import load_training_data
from solar_wind.sw_utils import sw_utils as swu
import pandas as pd


def test_load_df_with_original_data():
    root_project_path = swu.get_conf_path(only_root_path=True)
    df = load_training_data.load_df_with_original_data(2000,
                                                       1,
                                                       root_project_path + "\\solar_wind\\test\\test_data_loading")
    assert df.shape == (100, 57)
