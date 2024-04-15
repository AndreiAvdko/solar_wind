import os
import datetime
import requests
import spaceweather as sw
import sw_utils as swu


def load_newest(path=None):
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
    url = "https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/extended/"
    try:
        response = requests.head(url, timeout=5)  # Отправляем HEAD запрос (без тела ответа) для экономии ресурсов
        if response.status_code == 200:  # Если получаем успешный код ответа
            return True
        else:
            return False
    except requests.ConnectionError("Resource not available or problem with network connection"):
        return False
