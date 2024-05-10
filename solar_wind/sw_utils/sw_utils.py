import json
import os

from matplotlib import pyplot as plt


def get_original_data_path(path=None):
    current_directory = get_conf_path(only_root_path=True)
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    original_data_path = current_directory + config_data['original_data_path']
    create_folder_if_not_exist(original_data_path)
    return original_data_path


def get_clean_data_path(path=None):
    current_directory = get_conf_path(only_root_path=True)
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    clean_data_path = current_directory + config_data['clean_data_path']
    create_folder_if_not_exist(clean_data_path)
    return clean_data_path


def get_model_path(path=None):
    current_directory = get_conf_path(only_root_path=True)
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    training_model_path = current_directory + config_data['training_model_path']
    create_folder_if_not_exist(training_model_path)
    return training_model_path


def get_model_file_name():
    with open(get_conf_path()) as file:
        config_data = json.load(file)
    model_file_name = config_data['model_file_name']
    return model_file_name


def get_start_data(path=None) -> int:
    with open(get_conf_path()) as file:
        config_data = json.load(file)
    start_year = config_data['start_year_loaded_data']
    return start_year


def get_predict_horizon() -> int:
    with open(get_conf_path()) as file:
        config_data = json.load(file)
    predict_horizon = config_data['predict_horizon']
    return predict_horizon


def get_dataset_var_set(path=None):
    """
    Метод получения списка названий обязательных колонок с данными для обучения модели или получения предсказания
    :param path: Путь к файлу конфигурации, по умолчанию используется путь к конфигурации в корне пакета
    :return: List[String]
    """
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    column_set = list(config_data['column_list'])
    return column_set


def get_target_list(path=None):
    """
    Метод получения списка названий обязательных колонок с данными для обучения модели или получения предсказания
    :param path: Путь к файлу конфигурации, по умолчанию используется путь к конфигурации в корне пакета
    :return: List[String]
    """
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    target_list = list(config_data['target'])
    return target_list


def get_regressors_list(path=None):
    """
    Метод получения списка названий обязательных колонок с данными для обучения модели или получения предсказания
    :param path: Путь к файлу конфигурации, по умолчанию используется путь к конфигурации в корне пакета
    :return: List[String]
    """
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    regressors_list = list(config_data['regressors_list'])
    return regressors_list


def get_upper_bound_outliers(path=None):
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    upper_bound = config_data['upper_bound_validate']
    return upper_bound


def get_lower_bound_outliers(path=None):
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    lower_bound = config_data['lower_bound_validate']
    return lower_bound


def create_folder_if_not_exist(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_conf_path(path=None, only_root_path=False) -> str:
    # TODO Удалить отладку
    print(f"Это абсолютный путь до скрипта: {os.path.dirname(os.path.abspath(__file__))}")

    if path is None:
        root_project_dir = os.path.dirname(os.path.abspath(__file__))  # TODO os.getcwd()
        while not os.path.exists(os.path.join(root_project_dir, 'project_conf.json')):
            # TODO Удалить отладку
            print(f"Проверяем этот путь {os.path.join(root_project_dir, 'project_conf.json')}")
            root_project_dir = os.path.dirname(root_project_dir)
        if only_root_path:
            # TODO удалить
            print(f"Вот корневая директория проекта: {root_project_dir}")
            return root_project_dir
        else:
            return root_project_dir + '\\project_conf.json'
    else:
        return path


# TODO метод для вывода данных о df, удалить
def print_df_data(title, df):
    print(title)
    print(df)


# TODO метод для отрисовки графика, удалить
def show_df_plot(plot_title, df):
    plt.plot(df)
    plt.title(plot_title)
    plt.show()
