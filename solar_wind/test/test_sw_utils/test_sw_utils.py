import os
import shutil
from solar_wind.sw_utils import sw_utils as swu


test_conf_path = "\\solar_wind\\test\\test_project_conf.json"


def test_get_conf_path():
    """
    Проверяем, что находится путь к файлу конфигурации тестового проекта из других директорий
    """
    conf_path = swu.get_conf_path()
    assert conf_path.endswith('\\project_conf.json')


def test_get_root_project_path():
    """
    Проверяем поиск корневой директории проекта
    """
    conf_path = swu.get_conf_path(only_root_path=True)
    assert conf_path.endswith('\\solar_wind')


def test_get_original_data_path():
    """
    Проверяем создание директории для хранения скачиваемых данных OMNIE о солнечном ветре
    """
    root_dir = swu.get_conf_path(only_root_path=True)
    assert root_dir.endswith('\\solar_wind')
    os.chdir(root_dir)
    if os.path.exists(root_dir + "\\original_data"):
        shutil.rmtree("original_data")

    original_data_path = swu.get_original_data_path()

    assert original_data_path.endswith('original_data\\')
    assert os.path.exists("original_data")


def test_get_clean_data_path():
    """
    Проверяем создание директории для хранения очищенных данных
    """
    root_dir = swu.get_conf_path(only_root_path=True)
    assert root_dir.endswith('\\solar_wind')
    os.chdir(root_dir)
    if os.path.exists(root_dir + "\\clean_data"):
        shutil.rmtree("clean_data")

    clean_data_path = swu.get_clean_data_path()

    assert clean_data_path.endswith('clean_data\\')
    assert os.path.exists("clean_data")


def test_get_model_path():
    """
    Проверяем создание директории для хранения модели
    """
    root_dir = swu.get_conf_path(only_root_path=True)
    assert root_dir.endswith('\\solar_wind')
    os.chdir(root_dir)
    if os.path.exists(root_dir + "\\model"):
        shutil.rmtree("model")

    training_model_path = swu.get_model_path()

    assert training_model_path.endswith('model\\')
    assert os.path.exists("model")


def test_get_start_data():
    """
    Проверяем корректность получения значения начальной даты
    """
    start_data = swu.get_start_data(test_conf_path)
    assert start_data == 2000


def test_get_dataset_var_set():
    """
    Проверяем получение данных из конфигурации о получении списка переменных для обучения
    """
    test_dir_path = os.getcwd()
    columns = swu.get_dataset_var_set(test_dir_path + test_conf_path)
    assert columns == ["AL", "AU", "AE"]


def test_get_upper_bound_outliers():
    """
    Проверяем получение данных из конфигурации о верхних допустимых границах значений
    """
    test_dir_path = os.getcwd()
    upper_bound_set = swu.get_upper_bound_outliers(test_dir_path + test_conf_path)
    assert upper_bound_set == {"AL": 0,
                               "AU": 1500
                               }


def test_get_lower_bound_outliers():
    """
    Проверяем получение данных из конфигурации о нижних допустимых границах значений
    """
    test_dir_path = os.getcwd()
    lower_bound_set = swu.get_lower_bound_outliers(test_dir_path + test_conf_path)
    assert lower_bound_set == {"AL": -3000,
                               "AU": 0,
                               }


