import yfinance as yf  # импорт библиотеки yfinance с использованием псевдонима yf - предоставляет доступ к финансовым данным из Yahoo Finance.


def fetch_stock_data(ticker, period='1mo'):
    """Получает исторические данные об акциях для указанного тикера и временного периода. Возвращает DataFrame с данными.
    Тикер — это краткое название в биржевой информации котируемых инструментов (акций, облигаций, индексов).
    Является уникальным идентификатором в рамках одной биржи или информационной системы. Используется для того,
    чтобы постоянно не печатать в сводках полное наименование ценных бумаг или других объектов торговли.
    DataFrame - структура хранения данных, организованных в двух изменениях(строках и столбцах)
    и соответствующих этим строкам и столбцам меток """
    stock = yf.Ticker(ticker)  # создаём объект модуля Ticker с заданным тикером.
    # Модуль Ticker позволяет получить список последних финансовых новостей по заданному тикеру.
    data = stock.history(period=period)  # получаем исторические данные об акциях для указанного тикера и временного периода.
    return data  # возвращаем DataFrame с данными


def add_moving_average(data, window_size=5):
    """Добавляет в DataFrame колонку со скользящим средним, рассчитанным на основе цен закрытия(столбец Close).
    Получает DataFrame с данными и размер окна window_size (количество наблюдений, включенных в среднее)
    Скользящее среднее (также называемое "простое скользящее среднее" или "конечное скользящее среднее")
    представляет собой среднее арифметическое значение наблюдений в определенном окне или периоде,
    который "скользит" вдоль временного ряда. Метод rolling(), создаёт скользящее окно для проведения операции на окне данных.
    Скользящее окно имеет размер window_size и перемещается по временному ряду с одним шагом за раз. Метод mean(),
    указывает, что скользящее среднего необходимо вычислить для конкретного элемента - столбца Close"""
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data


def calculate_and_display_average_price(data):
    """Вычисляет и выводит среднюю цену закрытия акций за заданный период.
    Получает DataFrame с колонкой скользящего среднего значения столбца Close.
    Метод mean вычисляет среднее значение строк столбца Close. Параметр axis - определяет направление выполнения операций
    axis=0 - движение вниз по строкам"""
    average_price = data['Close'].mean(axis=0)
    print(f'СРЕДНЯЯ ЦЕНА ЗАКРЫТИЯ АКЦИЙ ЗА ЗАДАННЫЙ ПЕРИОД:":  {average_price}\n')


def notify_if_strong_fluctuations(data, threshold):
    """Анализирует данные и уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.
    Получает DataFrame с данными за указанный период и заданный пользователем порог колебаний цены в процентах
    """
    list_prices_close = data['Close'].tolist()  # получаем список значений закрытия из столбца Close(DataFrame) за указанный период
    max_price, min_price = max(list_prices_close), min(list_prices_close)  # определяем минимальное и максимальное
    # значение полученного списка значений закрытия (столбец Close(DataFrame))
    average_price = (max_price + min_price) / 2  # определяем среднее значение цены между минимальной и максимальной
    # ценой закрытия
    percent_average_price = average_price * 0.01  # определяем 1 процент от средней цены между минимальной и максимальной
    # ценой закрытия
    float_threshold = float(threshold)  # переводим введённое значение допустимого колебания цены от пользователя(str)
    # в число с плавающей запятой(float)
    acceptable_fluctuation = percent_average_price * float_threshold  # определяем допустимое колебание цены акции
    min_acceptable_price = average_price - acceptable_fluctuation  # определяем минимально допустимую цену акции
    max_acceptable_price = average_price + acceptable_fluctuation  # определяем максимально допустимую цену акции
    for price in list_prices_close:  # перебираем список значений закрытия из столбца Close(DataFrame) за указанный период
        if price > max_acceptable_price:  # если цена закрытия больше максимально допустимой цены акции
            print(f'ПРЕВЫШЕН ПОРОГ КОЛЕБАНИЙ ЦЕНЫ ЗАКРЫТИЯ, ЦЕНА АКЦИИ ПОДНЯЛАСЬ НА {(price - average_price) / percent_average_price}%')
        elif price < min_acceptable_price:  # если цена закрытия меньше минимально допустимой цены акции
            print(f'ПРЕВЫШЕН ПОРОГ КОЛЕБАНИЙ ЦЕНЫ ЗАКРЫТИЯ, ЦЕНА АКЦИИ ОПУСТИЛАСЬ НА {(average_price - price) / percent_average_price}%')
        else:
            print(f'КОЛЕБАНИЕ ЦЕНЫ АКЦИЙ, НАХОДИЛОСЬ В ПРЕДЕЛАХ УКАЗАННОГО ДОПУСТИМОГО ПОРОГА КОЛЕБАНИЙ {float_threshold}%')

