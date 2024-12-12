Задача №3. Реализовать функционал: Экспорт данных в CSV
файл main.pu 

    import data_download as dd  # импорт из файла data_download результатов работы функций


    def main():
    """ Основная функция, управляющая процессом загрузки, обработки данных и их визуализации. Запрашивает
     у пользователя ввод данных, вызывает функции загрузки и обработки данных, а затем передаёт результаты
      на визуализацию.
    """
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), "
          "MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")

    ticker = input("ВВЕДИТЕ ТИКЕР АКЦИИ:»")

    print("Вот несколько примеров введения периода данных: '1d'(1 день), '5d'(5 дней), '1mo'(1 месяц), '3mo'(3 месяца),"
          " '6mo'(6 месяцев), '1y'(1 год), '2y'(2 года), '5y'(5 лет), '10y'(10 лет), 'ytd'(с начала года), "
          " 'max'(максимум): ")

    period = input("ВВЕДИТЕ ПЕРИОД АНАЛИЗА ДАННЫХ:»")

    # Получение данных о запасах, функция fetch_stock_data файл data_download
    stock_data = dd.fetch_stock_data(ticker, period)

    # Добавление скользящего среднего значение к данным, функция add_moving_average файл data_download
    stock_data = dd.add_moving_average(stock_data)

    # Вычисление среднего значение колонки 'Close'(Закрытие). Результат выводится в консоль.
    # Функция calculate_and_display_average_price файл data_download
    dd.calculate_and_display_average_price(stock_data)

    # Уведомление о сильных колебаниях, если цена акций колебалась более чем на заданный процент за период
    # Функция notify_if_strong_fluctuations файл data_download
    threshold = input("ВВЕДИТЕ ПОРОГ КОЛЕБАНИЙ ЦЕНЫ В ПРОЦЕНТАХ:»")
    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Сохранение данных об акциях в CSV файл
    # Функция export_data_to_csv файл data_download
    filename = 'dataframe'
    dd.export_data_to_csv(stock_data, filename)


    # Запуск процесса
    if __name__ == "__main__":
    main()

файл data_download.pu

    import yfinance as yf  # импорт библиотеки yfinance с использованием псевдонима yf - предоставляет доступ к финансовым
    # данным из Yahoo Finance.
    import pandas as pd  # импорт библиотеки Pandas - мощный инструмент для анализа и обработки табличных данных
    # (pd- общепринятое сокращение для Pandas в коде)
    from tabulate import tabulate  # импорт библиотеки tabulate - красивое оформление таблицы


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
    return data  # возвращаем DataFrame с дополнительным столбцом Moving_Average


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
            print(f'ПРЕВЫШЕН ПОРОГ КОЛЕБАНИЙ ЦЕНЫ ЗАКРЫТИЯ, ЦЕНА АКЦИИ ПОДНЯЛАСЬ НА {((price - average_price) / percent_average_price):.4f}%')
        elif price < min_acceptable_price:  # если цена закрытия меньше минимально допустимой цены акции
            print(f'ПРЕВЫШЕН ПОРОГ КОЛЕБАНИЙ ЦЕНЫ ЗАКРЫТИЯ, ЦЕНА АКЦИИ ОПУСТИЛАСЬ НА {((average_price - price) / percent_average_price):.4f}%')
        else:
            print(f'КОЛЕБАНИЕ ЦЕНЫ АКЦИЙ, НАХОДИЛОСЬ В ПРЕДЕЛАХ УКАЗАННОГО ДОПУСТИМОГО ПОРОГА КОЛЕБАНИЙ {float_threshold}%')


    def export_data_to_csv(data, filename):
    """Экспортирует полученные данные об акциях в CSV файл.
    Получает DataFrame с данными за указанный период и дополнительным столбцом Moving_Average и название CSV файла
    """
    data.to_csv('dataframe.csv')  # преобразуем полученную DataFrame в CSV файл(функция to_csv) с названием dataframe
    df = pd.read_csv('dataframe.csv')  # читаем CSV файл(функция read_csv) с названием dataframe
    headers = ['№', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'Moving_Average']
    # назначаем название столбцов
    print('************************ПОЛУЧЕННЫЕ ДАННЫЕ ОБ АКЦИЯХ************************')
    print(tabulate(df, headers=headers, tablefmt='grid', stralign='center'))  # выводим в консоль,
    # сохранённую DataFrame из CSV файл с названием dataframe


![2024-12-12_16-05-02](https://github.com/user-attachments/assets/12465f3c-3f1e-4cb0-9dc6-cecaa4329389)

