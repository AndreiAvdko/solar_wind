from solar_wind.custom_exception import MissingColumnsError, IncorrectTimestamps
import datetime
import pandas as pd
from solar_wind.sw_utils import sw_utils as swu
import numpy as np


class DataValidator:
    """
    Класс для выполнения проверки исходных данных перед обучением.
    """
    __df = pd.DataFrame()

    @staticmethod
    def check_and_clean_data(df: pd.DataFrame, fill_missing_by_interpolate=False) -> pd.DataFrame:
        """
        Последовательный вызов методов для проверки данных
        Args:
        df (pd.Dataframe): Параметр, представляющий собой dataframe с данными о солнечном ветре.
        fill_missing_by_interpolate (bool): Заполнять ли пропущенные значения линейной интерполяцией
        :return: pandas.DataFrame с очищенными данными
        """
        validator = DataValidator()
        validator.__df = df
        clean_df = ((validator
                     .__check_columns()
                     .__check_and_process_timestamp()
                     .__check_and_process_outliers()
                     .__check_missing_values(fill_missing_by_interpolate))
                    .__df)
        clean_df.to_csv(f'{swu.get_clean_data_path()}clean_data_for_predict_from_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.csv', index=True)
        return clean_df

    def __check_and_process_timestamp(self):
        """
        Функция проверки временных меток датафрейма.
        Дополняет пропущенные метки, заполняя пропущенные значения для столбцов на NaN
        Упорядочивает временные метки
        """
        try:
            self.__df.index = pd.to_datetime(self.__df.index)
        except:
            raise IncorrectTimestamps("Check timestamps format. It should be in format YYYY-MM-DD HH:MM:SS")
        try:
            # Преобразование индекса в почасовой формат
            # Если отсуствуют временные метки, обрабатываем заменой отсуствующих меток интерполяцией
            # И заполнением значений для стоблцов на NaN
            self.__df.index.freq = 'H'
        except:
            original_index = self.__df.index
            self.__df = self.__df.resample('H').interpolate(method='linear')
            changed_index = self.__df.index
            interpolated_rows = changed_index.difference(original_index)
            # Заменяем значения для интерполированных строк на NaN
            for index in interpolated_rows:
                self.__df.loc[index, self.__df.columns != self.__df.index.name] = None
        return self

    def __check_and_process_outliers(self):
        """
        Функция замены всех выбросов на NaN
        """
        lower_bound = swu.get_lower_bound_outliers()
        upper_bound = swu.get_upper_bound_outliers()

        # Заменяем все значения вне заданных границ на NaN
        for column in self.__df.columns:
            if column in lower_bound:
                self.__df.loc[(self.__df[column] < lower_bound[column]) | (
                            self.__df[column] > upper_bound[column]), column] = np.nan
        return self

    def __check_missing_values(self, fill_missing_by_interpolate=False):
        """
        Функция обработки пропущенных значений
        :param fill_missing_by_interpolate: заполнять значения интерполяцией или как NaN
        """
        if fill_missing_by_interpolate:
            self.__df.replace("", np.nan, inplace=True)
            self.__df.fillna(self.__df.interpolate(method='linear'), inplace=True, limit=0)
            # Если были пропущены первые значения - заполняем последующими непропущенными значениями в столбце
            self.__df.fillna(self.__df.interpolate(method='backfill'), inplace=True)
        return self

    def __check_columns(self):
        """
        Функция проверки наличия необходимых колонок с данными.
        Удаляет лишние колонки, оставляя указанные в test_project_conf.json
        """
        expected_columns = swu.get_dataset_var_set()
        missing_columns = [col for col in expected_columns if col not in self.__df.columns]
        if missing_columns:
            raise MissingColumnsError(f"The following columns are missing: {', '.join(missing_columns)}")

        # Удаление столбцов, которые не содержатся в expected_columns
        columns_to_drop = [col for col in self.__df.columns if col not in expected_columns]
        self.__df.drop(columns=columns_to_drop, inplace=True)
        return self
