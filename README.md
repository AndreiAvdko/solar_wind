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
- ```load_newest_data()``` для загрузки последних доступных исторических данных о солнечном ветре с ресурса [NASA](https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/)
- ```get_forecast(df=df, with_plot=True, real_values=real_values)``` для получения прогноза

Примеры использования функций представлены далее в инструкции


### Пример подготовленных для данных для получения прогноза значения скорости солнечного ветра
Для получения прогноза солнечного ветра на последующие 72 часа необходимо, чтобы передаваемый df с данными содержал исторические значения для всех переменных регрессоров, объявленных в конфигурационном файле ```test_project_conf.json```
Список необходимых переменных представлен в следующей таблице.

||n_plasma                     |n_p   |v_plasma                                     |p_flow| Kp    |R   |Dst  |AE   |f107_adj|AL    |AU   |
|------|-----------------------------|------|---------------------------------------------|------|-------|----|-----|-----|--------|------|-----|
|2000-01-01 00:00:00|15.0 |2.9   |675.0 |2.64  | 5.30  |71.0|-45.0|517.0|125.6   |-279.0|238.0|
|2000-01-01 01:00:00|15.0 |2.6   |677.0 |2.38  | 5.30  |71.0|-37.0|313.0|125.6   |-146.0|167.0|
|2000-01-01 02:00:00|16.0 |2.2   |708.0 |2.21  | 5.30  |71.0|-37.0|559.0|125.6   |-422.0|137.0|
|2000-01-01 03:00:00|15.0 |2.1   |706.0 |2.09  | 4.7   |71.0|-41.0|567.0|125.6   |-429.0|138.0|
|2000-01-01 04:00:00|15.0 |2.0   |721.0 |2.08  | 4.7   |71.0|-45.0|287.0|125.6   |-191.0|96.0 |

Детальное описание колонок, [представленных в исходных данных](https://spdf.gsfc.nasa.gov/pub/data/omni/low_res_omni/omni2.text) можно найти в следующей таблице:
<details><summary>Описание колонок в исходных данных</summary>

|Название столбца|WORD|FORMAT|Fill Value|MEANING                                         |Translation                                                                            |UNITS/COMMENTS                                                            |
|----------------|----|------|----------|------------------------------------------------|---------------------------------------------------------------------------------------|--------------------------------------------------------------------------|
|year            |1   |I4    |          |Year                                            |Год 1963, 1964 и т. д.                                                                 |1963, 1964, etc.                                                          |
|doy             |2   |I4    |          |Decimal Day                                     |Десятичный день 1 января = день 1                                                      |January 1 = Day 1                                                         |
|hour            |3   |I3    |          |Hour                                            |Час 0, 1,...,23                                                                        |0, 1,...,23                                                               |
|bsrn            |4   |I5    |9999      |Bartels rotation number                         |Число вращения Бартеля                                                                 |                                                                          |
|id_imf          |5   |I3    |99        |ID for IMF spacecraft                           |Идентификатор космического корабля ММП                                                 |See table                                                                 |
|id_sw           |6   |I3    |99        |ID for SW plasma spacecraft                     |Идентификатор плазменного космического корабля СВ                                      |See table ы                                                               |
|n_imf           |7   |I4    |999       |# of points in the IMF averages                 |Число точек в средних значениях ММП                                                    |                                                                          |
|n_plasma        |8   |I4    |999       |# of points in the plasma averages              |Число точек в плазме в среднем                                                         |                                                                          |
|B_mag_avg       |9   |F6.1  |999.9     |Field Magnitude Average &#124;B&#124;                     |Средняя величина поля &#124;B&#124; 1/N SUM &#124;B&#124;, нТл                                             |1/N SUM &#124;B&#124;, nT                                                           |
|B_mag           |10  |F6.1  |999.9     |Magnitude of Average Field Vector               |Величина среднего вектора поля sqrt(Bx^2+By^2+Bz^2)                                    |sqrt(Bx^2+By^2+Bz^2)                                                      |
|theta_B         |11  |F6.1  |999.9     |Lat.Angle of Aver. Field Vector                 |Шир.угол ср. Градусы вектора поля (координаты GSE)                                     |Degrees (GSE coords)                                                      |
|phi_B           |12  |F6.1  |999.9     |Long.Angle of Aver.Field Vector                 |Длинный угол среднего вектора поля в градусах (координаты GSE)                         |Degrees (GSE coords)                                                      |
|B_x             |13  |F6.1  |999.9     |Bx GSE, GSM                                     |Bx GSE, GSM                                                                            |nT                                                                        |
|B_y_GSE         |14  |F6.1  |999.9     |By GSE                                          |By GSE                                                                                 |nT                                                                        |
|B_z_GSE         |15  |F6.1  |999.9     |Bz GSE                                          |Bz GSE                                                                                 |nT                                                                        |
|B_y_GSM         |16  |F6.1  |999.9     |By GSM                                          |By GSM                                                                                 |nT                                                                        |
|B_z_GSM         |17  |F6 1  |999.9     |Bz GSM                                          |Bz GSM                                                                                 |nT                                                                        |
|sigma_B_mag_avg |18  |F6.1  |999.9     |sigma&#124;B&#124;                                        |сигма&#124;B&#124; Среднеквадратичное стандартное отклонение по средней величине                 |RMS Standard Deviation in average (magnitude (word 10), nT)               |
|sigma_B_mag     |19  |F6.1  |999.9     |sigma B                                         |sigma B Среднеквадратичное стандартное отклонение в векторе поля                       |RMS Standard Deviation in field (vector, nT (**))                         |
|sigma_B_x_GSE   |20  |F6.1  |999.9     |sigma Bx                                        |sigma Bx Среднеквадратичное стандартное отклонение Bx в среднем по X-компоненте GSE    |RMS Standard Deviation in GSE ( X-component average, nT )                 |
|sigma_B_y_GSE   |21  |F6.1  |999.9     |sigma By                                        |sigma By По среднеквадратическому стандартному отклонению в среднем по Y-компоненте GSE|RMS Standard Deviation in GSE (Y-component average, nT )                  |
|sigma_B_z_GSE   |22  |F6.1  |999.9     |sigma Bz                                        |sigma Bz Среднеквадратичное стандартное отклонение в среднем по Z-компоненту GSE       |RMS Standard Deviation in GSE (Z-component average, nT )                  |
|T_p             |23  |F9.0  |9999999.  |Proton temperature                              |Температура протона Градусы, К                                                         |Degrees, K                                                                |
|n_p             |24  |F6.1  |999.9     |Proton Density                                  |Плотность протонов Н/см^3                                                              |N/cm^3                                                                    |
|v_plasma        |25  |F6.0  |9999.     |Plasma (Flow) speed                             |Скорость плазмы (потока) км/с                                                          |km/s                                                                      |
|phi_v           |26  |F6.1  |999.9     |Plasma Flow Long. Angle                         |Угол долготы плазменного потока (Углы широты и долготы потока плазмы солнечного ветра обычно    измеряются по радиусу-вектору от Солнца)|Degrees, quasi-GSE*                                                       |
|theta_v         |27  |F6.1  |999.9     |Plasma  Flow Lat. Angle                         |Угол широты плазменного потока (Углы широты и долготы потока плазмы солнечного ветра обычно    измеряются по радиусу-вектору от Солнца)|Degrees, GSE*                                                             |
|n_alpha_n_p     |28  |F6.3  |9.999     |Na/Np                                           |Отношение Na/Np Альфа/Протон                                                           |Alpha/Proton ratio                                                        |
|p_flow          |29  |F6.2  |99.99     |Flow Pressure                                   |Давление потока P (нПа)                                                                |P (nPa)                                                                   |
|sigma_T         |30  |F9.0  |9999999.  |sigma T                                         |сигма T Градусы, К                                                                     |Degrees, K                                                                |
|sigma_n         |31  |F6.1  |999.9     |sigma N                                         |сигма NN/см^3                                                                          |N/cm^3                                                                    |
|sigma_v         |32  |F6.0  |9999.     |sigma V                                         |сигма V км/с                                                                           |km/s                                                                      |
|sigma_phi_v     |33  |F6.1  |999.9     |sigma phi V                                     |сигма фи V Градусы                                                                     |Degrees                                                                   |
|sigma_theta_v   |34  |F6.1  |999.9     |sigma theta V                                   |сигма тета V Градусы                                                                   |Degrees                                                                   |
|sigma_na_np     |35  |F6.3  |9.999     |sigma-Na/Np                                     |сигма-Na/Np                                                                            |                                                                          |
|E               |36  |F7.2  |999.99    |Electric field                                  |Электрическое поле                                                                     |-[V(km/s) * Bz (nT, GSM)] * 10**-3. (mV/m)                                |
|beta_plasma     |37  |F7.2  |999.99    |Plasma beta                                     |Бета плазмы Бета                                                                       |Beta = [(T*4.16/10**5) + 5.34] * Np / B**2                                |
|mach            |38  |F6.1  |999.9     |Alfven mach number                              |Число Маха Альвена                                                                     |Ma = (V * Np**0.5) / 20 * B                                               |
|Kp              |39  |I3    |99        |Kp                                              |Kp Индекс планетарной геомагнитной активности                                          |Planetary Geomagnetic Activity Index (e.g. 3+ = 33, 6- = 57, 4 = 40, etc.)|
|R               |40  |I4    |999       |R                                               |Число солнечных пятен                                                                  |Sunspot number (new version 2)                                            |
|Dst             |41  |I6    |99999     |DST Index                                       |Индекс летнего времени nT                                                              |nT, from Kyoto                                                            |
|AE              |42  |I5    |9999      |AE-index                                        |Индекс AE nT, из Киото                                                                 |nT, from Kyoto                                                            |
|p_01MeV         |43  |F10.2 |999999.99 |Proton flux                                     |Число потока протонов/см² сек ср >1 Мэв                                                |number/cmsq sec sr >1 Mev                                                 |
|p_02MeV         |44  |F9.2  |99999.99  |Proton flux                                     |Число потока протонов/см² сек ср >2 Мэв                                                |number/cmsq sec sr >2 Mev                                                 |
|p_04MeV         |45  |F9.2  |99999.99  |Proton flux                                     |Число потока протонов/см² сек ср >4 Мэв                                                |number/cmsq sec sr >4 Mev                                                 |
|p_10MeV         |46  |F9.2  |99999.99  |Proton flux                                     |Число потока протонов/см2 с ср >10 Мэв                                                 |number/cmsq sec sr >10 Mev                                                |
|p_30MeV         |47  |F9.2  |99999.99  |Proton flux                                     |Число потока протонов/см2 с ср >30 Мэв                                                 |number/cmsq sec sr >30 Mev                                                |
|p_60MeV         |48  |F9.2  |99999.99  |Proton flux                                     |Число потока протонов/см2 с ср >60 Мэв 49                                              |number/cmsq sec sr >60 Mev                                                |
|flag            |49  |I3    |0         |Flag(***)                                       |Если флаг равен 0, данные о потоке протонов отсутствуют или все данные о потоке протонов загрязнены магнитосферными событиями|(-1,0,1,2,3,4,5,6)                                                        |
|Ap              |50  |I4    |999       |ap-index                                        |ap-индекс, нТл                                                                         |nT                                                                        |
|f107_adj        |51  |F6.1  |999.9     |f10.7_index                                     |f10.7_index                                                                            |( sfu = 10-22W.m-2.Hz-1)                                                  |
|PC              |52  |F6.1  |999.9     |PC(N) index                                     |Индекс PC(N)                                                                           |                                                                          |
|AL              |53  |I6    |99999     |AL-index, from Kyoto                            |AL-индекс, нТл, из Киото                                                               |nT                                                                        |
|AU              |54  |I6    |99999     |AU-index, from Kyoto                            |AU-индекс, нТл, из Киото                                                               |nT                                                                        |
|mach_mag        |55  |F5.1  |99.9      |Magnetosonic mach number= = V/Magnetosonic_speed|Магнитозвуковое число Маха                                                             |                                                                          |
|QI_p            |    |      |          |                                                |Протон QI == солнечный ветер                                                           |                                                                          |


</details>

Также пример csv-файла подготовленный для получения предсказания можно найти в следующей директории репозитория:
```/jupiter_notebooks/validation_data/``` c названием ```values_for_predict.csv```
В файле ```values_for_predict.csv``` по тому же пути находятся реальные значения с которыми можно сравнить полученное предсказание.

Для получения предсказания необходимо скачать файлы с данными (или использовать свои подготовленные данные в соответствующем формате) выполнить следующий код:
```python
import solar_wind.solar_wind as sw
import pandas as pd

df = pd.read_csv("PATH_TO_FILE\\values_for_predict.csv", index_col=0)
predict = sw.get_forecast(df)

print(predict)
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

### Чтобы отдельно получить очищенные данные в формате .csv можно воспользоваться следующим кодом
```python
from solar_wind.load_trainig_data import load_training_data
from solar_wind.data_validation import DataValidator

# указываем год начала для данных и количество лет за которые нужно получить данные
df = load_training_data.load_df_with_original_data(start=2000,
                                                   year_count=19)

df = DataValidator.check_and_clean_data(df)
df.to_csv("PATH\\filename.csv")
```

### Обучение своей модели
Для экспериментов или обучения модели машинного обучения, используемой для предсказания со своими параметрами, можно воспользоваться Jupyter-блокнотами, расположенными в директории **jupiter_notebooks/** данного репозитория. 
После получения архива с моделью необходимо скопировать его в директорию модуля **model/**, установленного на локальной машине, в случае необходимости указать в файле конфигурации дополнительные переменные регрессоры и правильное имя для файла модели. 

