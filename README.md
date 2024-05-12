### Для установки модуля необходимо использовать следующую команду:
```pip install git+https://github.com/AndreiAvdko/solar_wind.git```

### Для импортирования установленного модуля
```import solar_wind.solar_wind as sw```

Допустимые версии python для использования модуля: ```от 3.8.0 до 3.11.0```, тестирование и проверка работы модуля проводилась на версии ```python=3.10.14```

### Для запуска тестов
В корне репозитория необходимо в консоли выполнить команду
```
> pytest
```

### Предоставляемые функции
- ```sw.load_newest_data()``` для загрузки последних доступных исторических данных о солнечном ветре с ресурса [NASA](https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/)
- 


### Пример подготовленных для данных для получения прогноза значения скорости солнечного ветра
Для получения прогноза солнечного ветра на последующие 72 часа необходимо, чтобы передаваемый df с данными содержал исторические значения для всех переменных регрессоров, объявленных в конфигурационном файле ```test_project_conf.json```
Список необходимых переменных представлен в следующей таблице.

||n_plasma                     |n_p   |v_plasma                                     |p_flow|Kp               |R   |Dst  |AE   |f107_adj|AL    |AU   |
|------|-----------------------------|------|---------------------------------------------|------|-----------------|----|-----|-----|--------|------|-----|
|2000-01-01 00:00:00|15.0                         |2.9   |675.0                                        |2.64  |5.300000000000001|71.0|-45.0|517.0|125.6   |-279.0|238.0|
|2000-01-01 01:00:00|15.0                         |2.6   |677.0                                        |2.38  |5.300000000000001|71.0|-37.0|313.0|125.6   |-146.0|167.0|
|2000-01-01 02:00:00|16.0                         |2.2   |708.0                                        |2.21  |5.300000000000001|71.0|-37.0|559.0|125.6   |-422.0|137.0|
|2000-01-01 03:00:00|15.0                         |2.1   |706.0                                        |2.09  |4.7              |71.0|-41.0|567.0|125.6   |-429.0|138.0|
|2000-01-01 04:00:00|15.0                         |2.0   |721.0                                        |2.08  |4.7              |71.0|-45.0|287.0|125.6   |-191.0|96.0 |

Также пример csv-файла подготовленный для получения предсказания можно найти в следующей директории репозитория:
```/jupiter_notebooks/validation_data/``` c названием ```values_for_predict.csv```
В файле ```values_for_predict.csv``` по тому же пути находятся реальные значения с которыми можно сравнить полученное предсказание.

Для получения предсказания необходимо скачать файлы с данными (или использовать свои подготовленные данные в соответствующем формате) выполнить следующий код:
```python
import solar_wind.solar_wind as sw
import pandas as pd

df = pd.read_csv("PATH_TO_FILE\\values_for_predict.csv", index_col=0)
predict = sw.get_forecast(df)

print(predict['segment_0']['target'])
# или для сохранения полученного предсказания в файл csv:
predict['segment_0']['target'].to_csv("PATH_TO_CSV_FILE")
```

### Для отрисовки графика можно использовать следующий пример:
```python
import solar_wind.solar_wind as sw
import pandas as pd

df = pd.read_csv("PATH_TO_FILE\\values_for_predict.csv",
                 index_col=0)
real_values = pd.read_csv(
    "PATH_TO_FILE\\real_values.csv", index_col=0)
real_values.index = pd.to_datetime(real_values.index)
real_values.set_index(pd.to_datetime(real_values.index), 
                      inplace=True)
 
predict = sw.get_forecast(df=df,
                          with_plot=True,
                          real_values=real_values
                          )
print(predict)
```

Как видно из примера функция ```get_forecast()``` позволяет передать известные значения, для получаемого предсказания, которые также будут участвовать в отрисовке графика.
При отсутствии этого параметра они не будут отрисованы на графике предсказания.

### Загрузка сохраненных данных о солнечном ветре в виде готового Dataframe
После загрузки данных их можно загрузить и использовать с помощью следующей функции, реализованной в модуле.
Для этого необходимо передать год, начиная с которого будут загружаться данные, а также количество лет, начиная с этого года.
```python
from solar_wind.load_trainig_data import load_training_data

df = load_training_data.load_df_with_original_data(start=2000, 
                                                   year_count=1)
```
