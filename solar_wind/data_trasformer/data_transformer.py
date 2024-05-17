import warnings
warnings.filterwarnings('ignore')
from etna.datasets.tsdataset import TSDataset
import pandas as pd


def dataframe_to_TSDataset(clean_df,
                           target_list,
                           regressors_list) -> TSDataset:
    """
    Функция преобразования исходного dataframe с данными в формат данных фреймворка ETNA
    :param clean_df: pandas dataframe с исходными данными
    :param target_list: список целевой переменной для предсказания
    :param regressors_list: список переменных регрессоров
    :return: TSDataset
    """
    # Получаем очищенные данные
    df = clean_df.copy()
    # Сбрасываем индекс и переименовываем в timestamp
    df = df.reset_index()
    df.rename(columns={'index': 'timestamp'}, inplace=True)
    # преобразовываем столбец timestamp в столбец с временными метками
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df_target = df[target_list]
    df_regressors = df[regressors_list]
    # Подготавливаем регрессоры
    if regressors_list:
        df_regressors.columns = ["timestamp"] + [f"regressor_{i}_{regressors_list[i + 1]}" for i in
                                                 range(len(regressors_list) - 1)]
        df_regressors["segment"] = "segment_0"
        df_regressors = TSDataset.to_dataset(df_regressors)
    # подготавливаем dataframe с целевой переменной
    df_target['target'] = df_target['v_plasma']
    df_target.drop(columns=['v_plasma'], inplace=True)
    df_target['segment'] = 'segment_0'
    # превращаем датафрейм
    # с плоским индексом в датафрейм с мультииндексом
    df_target = TSDataset.to_dataset(df_target)
    # превращаем датафрейм в объект TSDataset
    if not regressors_list:
        ts_target = TSDataset(df_target, freq='H')
    else:
        ts_target = TSDataset(df_target, freq='H', df_exog=df_regressors)
    return ts_target
