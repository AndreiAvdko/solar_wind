from сustom_exception.custom_exception import (EmptyDataFrameError,
                                               MissingColumnsError)
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import spaceweather as sw
import sw_utils as swu

import sw_utils


class DataValidator:
    __df = pd.DataFrame()

    @staticmethod
    def check_and_clean_data(df: pd.DataFrame) -> pd.DataFrame:
        """
        Последовательный вызов методов для проверки данных
        :return: pandas.DataFrame
        """
        # TODO реализовать функцию
        df = df

        # Вызываем методы в нужной последовательности
        #checker._load_df_with_original_data().
        print("call check_data")


    def _check_and_process_timestamp(self):
        # TODO реализовать функцию
        print("call check_and_process_timestamp")
        return self

    def _check_and_process_outliers(self):
        # TODO реализовать функцию
        print("call check_and_process_outliers")
        return self

    def _check_missing_values(self):
        # TODO реализовать функцию
        print("call check_missing_values")
        return self

    def _check_columns(self):
        expected_columns = sw_utils.get_dataset_var_set()
        missing_columns = [col for col in expected_columns if col not in self.df.columns]
        if missing_columns:
            raise MissingColumnsError(f"The following columns are missing: {', '.join(missing_columns)}")

    def _load_df_with_original_data(self,
                                    start=swu.get_start_data(),
                                    year_count=1,
                                    path=swu.get_original_data_path()):
        if start + year_count > datetime.datetime.now().year:
            raise ValueError("Impossible to get data. Check year count.")
        original_data_df = sw.omnie_hourly(start, cache=True, local_path=path)
        for i in range(year_count):
            if year_count == 1: break
            df_hplot = sw.omnie_hourly(start + i + 1, cache=True, local_path=path)
            original_data_df = pd.concat([original_data_df, df_hplot])
        self.df = original_data_df

        # TODO удалить функциональность отрисовки графика
        # отрисовываем график
        plt.plot(original_data_df[["v_plasma"]])
        plt.title(f"Значения скорости солнечного ветра за {start} - {start + year_count} гг.")
        plt.show()
        return self
