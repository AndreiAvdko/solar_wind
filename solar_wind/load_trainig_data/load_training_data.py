import os
import datetime
import matplotlib.pyplot as plt
import pandas as pd
import requests
import spaceweather as sw
from solar_wind.sw_utils import sw_utils as swu


def load_newest(path=None):
    """
    Функция загрузки последних данных о солнечном ветре.
    В качестве стартовой даты скачивания данных - дата указанная в конфигурационном файле проекта (project_conf.json)
    """
    check_omnie_resource_availability()
    if path is None:
        path = swu.get_original_data_path()
    if check_if_path_exists(path):
        # загружаем файл конфигурации и получаем начальное значение года
        # с которого начинаем скачивать данные с ресурса OMNIE
        start_year = swu.get_start_data()
        current_year = datetime.datetime.now().year
        # Скачиваем данные с ресурса
        for i in range(current_year - start_year + 1):
            try:
                sw.cache_omnie(start_year + i, local_path=path)
                # Консольный статус-бар состояния загрузки данных с ресурса
                progress = i * 100 // (current_year - start_year)
                bar = "#" * (progress // 5)
                print(f"\rProgress: [{bar:20s}] {progress}% ", end="", flush=True)
            except requests.exceptions.RequestException as e:
                print(f"\nError occurred while downloading data for {current_year + i} year: {e}")
                break
        print("\nData was loaded successfully")
    else:
        raise FileNotFoundError("Path does not exist. Check the path")


def check_if_path_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False


def check_omnie_resource_availability():
    """
    Функция проверки сетевого соединения с ресурсом получения данных о солнечном ветре
    """
    url = "https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/extended/"
    try:
        response = requests.head(url, timeout=5)  # Отправляем HEAD запрос (без тела ответа) для экономии ресурсов
        if response.status_code == 200:  # Если получаем успешный код ответа
            return True
        else:
            return False
    except requests.ConnectionError("Resource not available or problem with network connection"):
        return False


def load_df_with_original_data(start=swu.get_start_data(),
                               year_count=1,
                               path=swu.get_original_data_path()):
    """
    Функция получения датафрейма из загруженных данных о солнечном ветре
    :param start: Начальный год данных
    :param year_count: количество лет за которые нужно загрузить данные, начиная с даты start
    :param path: указание пути для данных, по умолчанию данные скачиваются и загружаются в папки проекта
    :return: DataFrame
    """
    if start + year_count > datetime.datetime.now().year:
        raise ValueError("Impossible to get data. Check year count.")
    original_data_df = sw.omnie_hourly(start, cache=True, local_path=path)
    for i in range(year_count):
        if year_count == 1: break
        df_hplot = sw.omnie_hourly(start + i + 1, cache=True, local_path=path)
        original_data_df = pd.concat([original_data_df, df_hplot])

    # TODO удалить функциональность отрисовки графика
    # # отрисовываем график
    # plt.plot(original_data_df[["v_plasma"]])
    # plt.title(f"Значения скорости солнечного ветра за {start} - {start + year_count} гг.")
    # plt.show()
    return original_data_df
