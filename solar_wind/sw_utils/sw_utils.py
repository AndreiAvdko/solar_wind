import warnings
warnings.filterwarnings('ignore')
import json
import os
import datetime
import pandas as pd
import warnings
from matplotlib import pyplot as plt



def get_original_data_path(path=None):
    """
    Функция получения пути к файлам с исходными данными формата .dat из файла конфигурации
    :return: path:String
    """
    current_directory = get_conf_path(only_root_path=True)
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    original_data_path = (current_directory +
                          get_delimiter() +
                          config_data['original_data_path'] +
                          get_delimiter())
    create_folder_if_not_exist(original_data_path)
    return original_data_path


def get_clean_data_path(path=None):
    """
    Функция получения пути к директории на диске для хранения очищенных данных из файла конфигурации
    :return: path:String
    """
    current_directory = get_conf_path(only_root_path=True)
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    clean_data_path = (current_directory +
                       get_delimiter() +
                       config_data['clean_data_path'] +
                       get_delimiter())
    create_folder_if_not_exist(clean_data_path)
    return clean_data_path


def get_model_path(path=None):
    """
    Функция получения пути к директории с архивом модели машинного обучения для получения прогноза из файла конфигурации
    :return: path:String
    """
    current_directory = get_conf_path(only_root_path=True)
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    training_model_path = (current_directory +
                           get_delimiter() +
                           config_data['training_model_path'] +
                           get_delimiter())
    create_folder_if_not_exist(training_model_path)
    return training_model_path


def get_prediction_artefacts_path(path=None):
    """
    Функция получения пути к директории для сохранения артефактов предсказания из файла конфигурации
    :return: path:String
    """
    current_directory = get_conf_path(only_root_path=True)
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    prediction_artefacts_path = (current_directory +
                                 get_delimiter() +
                                 config_data['prediction_artefacts_path'] +
                                 get_delimiter())
    create_folder_if_not_exist(prediction_artefacts_path)
    return prediction_artefacts_path


def get_model_file_name():
    """
    Функция получения названия файла с моделью машинного обучения из файла конфигурации
    :return: filename:String
    """
    with open(get_conf_path()) as file:
        config_data = json.load(file)
    model_file_name = config_data['model_file_name']
    return model_file_name


def get_start_data(path=None) -> int:
    """
    Функция получения начальной даты для загрузки исходных данных о солнечном ветре из файла конфигурации
    :return: start_year:String
    """
    with open(get_conf_path()) as file:
        config_data = json.load(file)
    start_year = config_data['start_year_loaded_data']
    return start_year


def get_predict_horizon() -> int:
    """
    Функция получения значения горизонта прогнозирования из файла конфигурации
    :return: predict_horizon:String
    """
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
    Метод получения списка названий обязательных колонок с данными для обучения модели или получения предсказания из файла конфигурации
    :return: List[String]
    """
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    regressors_list = list(config_data['regressors_list'])
    return regressors_list


def get_upper_bound_outliers(path=None):
    """
    Функция получения допустимых максимальных значений для переменных из файла конфигурации
    :return: List[String]
    """
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    upper_bound = config_data['upper_bound_validate']
    return upper_bound


def get_lower_bound_outliers(path=None):
    """
     Функция получения допустимых минимальных значений для переменных из файла конфигурации
    :param path:
    :return:
    """
    with open(get_conf_path(path)) as file:
        config_data = json.load(file)
    lower_bound = config_data['lower_bound_validate']
    return lower_bound


def create_folder_if_not_exist(folder_path):
    """
    Функция создания директории в случае ее отсутствия на диске
    :param folder_path: путь к директории
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def get_conf_path(path=None, only_root_path=False) -> str:
    """
    Функция получения пути к файлу с конфигурацией модуля
    :param only_root_path: Если True - получение абсолютного пути к корню проекта, если False - получение абсолютного пути к файлу с конфигурацией
    :return: path:String
    """
    if path is None:
        root_project_dir = os.path.dirname(os.path.abspath(__file__))
        while not os.path.exists(os.path.join(root_project_dir, 'project_conf.json')):
            root_project_dir = os.path.dirname(root_project_dir)
        if only_root_path:
            return root_project_dir
        else:
            return root_project_dir + '\\project_conf.json'
    else:
        return path



def show_df_plot(plot_title, prediction_df, df_with_was_predicted, real_values: pd.DataFrame = None):
    """

    :param plot_title: Название графика
    :param prediction_df: pandas.DataFrame c предсказанием
    :param df_with_was_predicted: pandas.DataFrame c данными для предсказания
    :param real_values: [OPTIONAL] pandas.DataFrame с реальными значениями, для отображения их на графике, применимо для тестирования функциональности модуля
    :return:
    """
    plt.plot(prediction_df,
             label="Предсказанные значения")
    plt.plot(df_with_was_predicted["v_plasma"].tail(20),
             label='Последние известные значения')
    if real_values is not None:
        plt.plot(real_values["v_plasma"],
                 label='Реальные значения')
    plt.title(plot_title)
    plt.legend()
    plt.savefig(f'{get_prediction_artefacts_path()}prediction_plot_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.png')
    plt.show()



def get_delimiter():
    delimiter = {"linux_delimiter": "/", "windows_delimiter": "\\"}
    if (os.name == "nt"):
        return delimiter.get('windows_delimiter')
    else:
        return delimiter.get('linux_delimiter')


def ignore_warnings(func):
    def wrapper(*args, **kwargs):
        warnings.filterwarnings('ignore')
        warnings.filterwarnings('ignore', category=UserWarning)
        warnings.filterwarnings('ignore', category=RuntimeWarning)
        return func(*args, **kwargs)
    return wrapper
