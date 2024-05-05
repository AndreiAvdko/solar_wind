from solar_wind.custom_exception import MissingColumnsError
from solar_wind.load_trainig_data import load_training_data
from solar_wind.sw_utils import sw_utils as swu
from solar_wind.data_validation import DataValidator
import pytest
import pandas as pd

testsuit_dataset_base_path = "\\solar_wind\\test\\test_data_validation\\test_data"


def test_check_columns():
    """
    Проверяем, функцию проверки наличия указанных в конфигурации столбцов и удаления лишних столбцов
    для dataframe со всеми присутствующими колонками
    """
    root_project_path = swu.get_conf_path(only_root_path=True)
    df = load_training_data.load_df_with_original_data(2000,
                                                       1,
                                                       root_project_path +
                                                       testsuit_dataset_base_path +
                                                       "\\all_required_column")
    assert df.shape == (2, 57)
    # print(f"Список исходных колонок {df.columns}")
    clean_df = DataValidator.check_and_clean_data(df)
    source_clean_columns = set(clean_df.columns)
    right_columns = set(swu.get_dataset_var_set())
    # Проверяем колонки, и размерность очищенного массива
    assert clean_df.shape == (2, len(right_columns))
    assert source_clean_columns == right_columns


def test_check_missing_columns():
    """
    Проверяем, выбрасывание исключения функцией проверки наличия указанных в конфигурации столбцов
    для dataframe c отсутствующей колонкой
    """
    root_project_path = swu.get_conf_path(only_root_path=True)
    df = pd.read_csv(root_project_path +
                     testsuit_dataset_base_path +
                     "\\missing_columns\\omni2_2000.csv")

    # Проверяем, что столбца AU нет в исходном df
    assert df.shape == (2, 11)
    assert 'v_plasma' not in df.columns
    # Проверяем выбрасывание исключения из-за отсутствия необходимого столбца
    with pytest.raises(MissingColumnsError):
        DataValidator.check_and_clean_data(df)


def test_check_loading_with_correct_timestamps():
    """
    Проверяем загрузку dataframe с корректными временными метками
    """
    root_project_path = swu.get_conf_path(only_root_path=True)
    df = pd.read_csv(root_project_path +
                     testsuit_dataset_base_path +
                     "\\correct_timestamps\\omni2_2000.csv",
                     index_col=0,
                     parse_dates=True)

    df = DataValidator.check_and_clean_data(df)
    assert df.shape == (9, 11)
    assert df.index.freq == 'H'
    # Проверяем отсутствие значений NaN
    assert not df.isnull().any().any()


def test_check_loading_and_filling_df_with_missing_intermediate_timestamps():
    """
    Проверяем заполнение индекса временных меток интерполяцией и пустыми значениями для колонок
    """
    root_project_path = swu.get_conf_path(only_root_path=True)
    df = pd.read_csv(root_project_path +
                     testsuit_dataset_base_path +
                     "\\missing_timestamps\\omni2_2000.csv",
                     index_col=0,
                     parse_dates=True)

    df = DataValidator.check_and_clean_data(df)

    assert df.shape == (9, 11)
    assert df.index.freq == 'H'
    # Проверяем, все ли значения в изначально отсутствующих строках NaN
    assert df.loc[['2000-01-01 04:00:00', '2000-01-01 06:00:00']].isnull().all(axis=1).all()


def test_check_and_process_outliers():
    """
    Проверяем функцию обработки выбросов.
    В проверочном датасете данные подобраны так, чтобы все строки начиная со 2 принимали значение NaN
    """
    root_project_path = swu.get_conf_path(only_root_path=True)
    df = pd.read_csv(root_project_path +
                     testsuit_dataset_base_path +
                     "\\with_outliers\\omni2_2000.csv",
                     index_col=0,
                     parse_dates=True)
    df = DataValidator.check_and_clean_data(df)

    # Выбираем строки начиная со второй строки
    # Проверяем, все ли значения в выбранных строках NaN
    selected_rows = df.iloc[2:]
    all_nan_after_second_row = selected_rows.isnull().all(axis=1).all()

    # Проверка размера и заполнение выбросов как NaN dataframe
    assert df.shape == (5, 11)
    assert all_nan_after_second_row, "Not all values after the second line are NaN"
    # Сохранение df в файл csv для просмотра значений
    # df.to_csv(root_project_path + testsuit_dataset_base_path + "\\with_outliers\\clean_from_outliers.csv")


test_data = [
    (False, 45),
    (True, 0),
]


@pytest.mark.parametrize("fill_missing_by_interpolate, expected", test_data)
def test_check_missing_values(fill_missing_by_interpolate, expected):
    """
    Проверяем функцию проверки и заполнения пропущенных значений c заполнением интерполяцией
    и без нее
    """
    root_project_path = swu.get_conf_path(only_root_path=True)
    df = pd.read_csv(root_project_path +
                     testsuit_dataset_base_path +
                     "\\missing_values\\omni2_2000.csv",
                     index_col=0,
                     parse_dates=True)
    # Проверяем кол-во пропущенных значений до заполнения
    assert df.shape == (9, 11)
    assert df.isnull().sum().sum() == 45

    df = DataValidator.check_and_clean_data(df,
                                            fill_missing_by_interpolate=fill_missing_by_interpolate)

    # Проверяем кол-во пропущенных значений после заполнения
    assert df.isnull().sum().sum() == expected
    assert df.shape == (9, 11)
    # Сохранение df в файл csv для просмотра значений
    #df.to_csv(root_project_path + testsuit_dataset_base_path + "\\missing_values\\clean_from_missing_values.csv")
