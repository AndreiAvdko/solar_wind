### Для установки модуля необходимо использовать следующую команду:
```pip install git+https://github.com/AndreiAvdko/solar_wind.git'''```

### Для импортирования установленного модуля
```import solar_wind.solar_wind as sw```

### Предоставляемые функции
- ```sw.load_newest_data()```


### Пример подготовленных для предсказания
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