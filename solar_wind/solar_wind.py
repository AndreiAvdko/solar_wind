import warnings
warnings.filterwarnings('ignore')
import datetime
import pandas as pd
from etna.core import load
from solar_wind.load_trainig_data import load_training_data as lt_data
from solar_wind.data_validation import DataValidator
from solar_wind.data_trasformer import data_transformer as data_trsfrm
from solar_wind.sw_utils import sw_utils as swu
from solar_wind.sw_utils.sw_utils import ignore_warnings


@ignore_warnings
def get_forecast(df: pd.DataFrame = None,
                 with_plot: bool = False,
                 real_values: pd.DataFrame = None) -> pd.DataFrame:
    """
    Функция получения предсказания о солнечном ветре
    :param df: pandas.DataFrame с данными для которых нужно получить предсказание
    :param with_plot: Опциональный параметр отрисовки графика с предсказаннием,
                      по умолчанию график не отрисовывается
    :return: pandas.DataFrame c прогнозом
    """
    if df is None:
        df = DataValidator.check_and_clean_data(lt_data.load_df_with_original_data())
    target_list = swu.get_target_list()
    regressors_list = swu.get_regressors_list()
    # Загружаем сохраненную модель
    pipe = load(swu.get_model_path() + swu.get_model_file_name())

    df_for_predict = DataValidator.check_and_clean_data(df, fill_missing_by_interpolate=True)
    df_for_predict = data_trsfrm.dataframe_to_TSDataset(df_for_predict,
                                                        target_list=target_list,
                                                        regressors_list=regressors_list)
    print("Получаем предсказание, это может занять какое-то время...")
    predict = pipe.forecast(df_for_predict)
    predict = predict.to_pandas()
    # Отрисовка графика
    if with_plot:
        swu.show_df_plot(plot_title="Предсказанные значения солнечного ветра",
                         prediction_df=predict['segment_0']['target'],
                         df_with_was_predicted=df,
                         real_values=real_values)
    predict['segment_0']['target'].to_csv(f'{swu.get_prediction_artefacts_path()}prediction_plot_{datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S")}.csv')
    return predict['segment_0']['target']


def load_newest_data():
    """
    Функция загрузки последних актуальных данных о солнечном ветре с ресурса OMNIE
    """
    lt_data.load_newest()