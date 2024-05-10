import pandas
import pandas as pd
from etna.core import load
from etna.analysis import plot_backtest
from etna.metrics import SMAPE, MSE, MAE
from etna.transforms import MeanTransform, StandardScalerTransform, LagTransform, MinMaxScalerTransform
import matplotlib.pyplot as plt
import solar_wind.solar_wind
from solar_wind.load_trainig_data import load_training_data as lt_data
from solar_wind.data_validation import DataValidator
from solar_wind.data_trasformer import data_transformer as data_trsfrm
from solar_wind.sw_utils import sw_utils as swu
from solar_wind.sw_utils.sw_utils import ignore_warnings
from etna.models import CatBoostPerSegmentModel, ElasticPerSegmentModel, LinearPerSegmentModel
from etna.pipeline import Pipeline, AutoRegressivePipeline


@ignore_warnings
def get_forecast(df: pd.DataFrame = None,
                 with_plot: bool = False,
                 real_values: pandas.DataFrame = None) -> pd.DataFrame:
    """
    Функция получения предсказания о солнечном ветре
    :param df: pandas.DataFrame с данными для которых нужно получить предсказание
    :param with_plot: Опциональный параметр отрисовки графика с предсказаннием,
                      по умолчанию график не отрисовывается
    :return: pandas.DataFrame с предсказанными значениями
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

    predict = pipe.forecast(df_for_predict)
    predict = predict.to_pandas()
    # TODO удалить
    predict.to_csv("C:\\Users\\andre\\PycharmProjects\\solar_wind\\predictions\\prediction.csv")
    # Отрисовываем график
    if with_plot:
        swu.show_df_plot(plot_title="Предсказанные значения солнечного ветра",
                         prediction_df=predict['segment_0']['target'],
                         df_with_was_predicted=df,
                         real_values=real_values)
    return predict['segment_0']['target']


def additional_model_training(iterations: int,
                              depth: int,
                              train_df: pd.DataFrame = None,
                              start_year: int = None,
                              end_year: int = None,
                              using_measure_points: int = None):
    """
    Функция дополнительного дообучения модели
    :param train_df: Данные для обучения модели. Опциональный параметр.
        Если не передан, то для обучения будут загружены последние данные с ресурса OMNIE.
        Настоятельно рекомендуется дообучать модель на своих проверенных данных,
        поскольку на ресурсе могут отсутствовать актуальные данные для переменных регрессоров, используемых для обучения
    :param end_year: TODO
    :param start_year: TODO
    :param using_measure_points: TODO
    """
    target_list = swu.get_target_list()
    regressors_list = swu.get_regressors_list()

    if train_df is None:
        solar_wind.solar_wind.load_newest_data()
        df = lt_data.load_df_with_original_data(start=start_year,
                                                year_count=end_year - start_year)
    else:
        df = train_df
    df = DataValidator.check_and_clean_data(df, fill_missing_by_interpolate=True)
    # TODO удалить сохранение датафрейма для обучения модели
    df.to_csv("C:\\Users\\andre\\PycharmProjects\\solar_wind\\predictions\\with_this_model_was_training.csv")

    etna_df = data_trsfrm.dataframe_to_TSDataset(df,
                                                 target_list=target_list,
                                                 regressors_list=regressors_list,
                                                 using_measure_points=using_measure_points)
    etna_df.to_pandas().to_csv(
        "C:\\Users\\andre\\PycharmProjects\\solar_wind\\predictions\\transformation_into_etna_result.csv")

    ############################################################################################
    ############################################################################################
    ###################################Модель CatBoost##########################################
    ############################################################################################
    ############################################################################################
    # model = CatBoostPerSegmentModel(iterations=iterations,
    #                                 depth=depth)
    # transforms = [
    #     MeanTransform(in_column='target',
    #                   window=80,
    #                   out_column='mean'),
    # ]
    #
    # if regressors_list:
    #     for i in range(len(regressors_list) - 1):
    #         mean_regressor = MeanTransform(in_column=f"regressor_{i}_{regressors_list[i + 1]}",
    #                                        window=80,
    #                                        out_column=f"mean_regressor_{i}__{regressors_list[i + 1]}")
    #         transforms.append(mean_regressor)

    ############################################################################################
    ############################################################################################
    ###################################Модель Линейной регрессии Elastic   #####################
    ############################################################################################
    ############################################################################################
    # model = ElasticPerSegmentModel(l1_ratio=0.7,
    #                                alpha=0.02,
    #                                random_state=42)
    #
    # transforms = [
    #     StandardScalerTransform('target'),
    #     LagTransform(
    #         in_column='target',
    #         lags=list(range(swu.get_predict_horizon(),
    #                         swu.get_predict_horizon() + 2)))
    # ]
    # # если список регрессоров не пуст, то добавляем лаги для них
    # if regressors_list:
    #     for i in range(len(regressors_list) - 1):
    #         lags_regressor = LagTransform(in_column=f"regressor_{i}_{regressors_list[i + 1]}",
    #                                       lags=list(range(swu.get_predict_horizon(),
    #                                                       swu.get_predict_horizon() + 2)))
    #         transforms.append(lags_regressor)

    ############################################################################################
    ############################################################################################
    ##############################     Модель Линейной регрессии           #####################
    ############################  Работает только с Autoregressive Pipeline ####################
    ############################################################################################
    model = LinearPerSegmentModel(fit_intercept=False)

    transforms = [
        MinMaxScalerTransform(in_column=None),
        LagTransform(in_column="target",
                     lags=list(range(1, swu.get_predict_horizon() + 1)))
    ]

    if regressors_list:
        for i in range(len(regressors_list) - 1):
            lags_regressor = LagTransform(in_column=f"regressor_{i}_{regressors_list[i + 1]}",
                                          lags=list(range(1, swu.get_predict_horizon() + 1)))
            transforms.append(lags_regressor)

    pipeline = AutoRegressivePipeline(model=model,
                                      transforms=transforms,
                                      horizon=swu.get_predict_horizon())
    # TODO удалить
    print("Обучаем модель на данных (начало + конец)")
    print(etna_df.head(3))
    print(etna_df.tail(3))
    pipeline.fit(etna_df)
    metrics_df, forecast_df, fold_info_df = pipeline.backtest(ts=etna_df,
                                                              metrics=[MAE(),
                                                                       MSE(),
                                                                       SMAPE()],
                                                              aggregate_metrics=True,
                                                              n_folds=5)
    plot_backtest(forecast_df, etna_df)
    plt.show(block=True)

    pipeline.save(swu.get_model_path() + swu.get_model_file_name())
    print("Модель обучена")
    return metrics_df
    # TODO реализовать сравнение точности с текущей моделью


def load_newest_data():
    """
    Функция загрузки последних актуальных данных о солнечном ветре с ресурса OMNIE
    """
    lt_data.load_newest()