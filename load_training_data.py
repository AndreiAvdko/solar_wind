import os
import time
import datetime
import requests
import spaceweather as sw
import json

def load_newest(path=''):
    if check_if_path_exists(path):
        # загружаем файл конфигурации и получаем начальное значение года
        # с которого начинаем скачивать данные с ресурса OMNIE
        with open('project_conf.json') as file:
            config_data = json.load(file)
        start_year = config_data['start_year_loaded_data']
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
                print(f"\nError occurred while downloading data for {current_year+i} year: {e}")
                break
        print("Data was loaded successfully")
    else:
        raise FileNotFoundError("Path does not exist")


def check_if_path_exists(path):
    if os.path.exists(path):
        return True
    else:
        return False
