import pandas as pd

# print(sw_utils.get_start_data())


# print(f"\n\n{os.getcwd()}\n\n")

# print(lt.check_omnie_resource_availability())



# df = spaceweather.omnie_hourly(2001, cache=True, local_path="C:\\Users\\andre\\PycharmProjects\\solar_wind\\original_data")
# from solar_wind.data_validation import data_validation

# df = pd.DataFrame()

# data_validation.DataValidator.check_and_clean_data(df)


# from solar_wind.load_trainig_data import load_training_data
#
# df = load_training_data.load_df_with_original_data()
# print(df.head())

# from solar_wind.sw_utils import sw_utils as swu
# expected_columns = swu.get_dataset_var_set()
# print(expected_columns)

from solar_wind.data_validation import DataValidator
import pandas

df = pandas.DataFrame()
DataValidator.check_and_clean_data(df)