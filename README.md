Задача №4. Реализовать функционал: Добавление дополнительных технических индикаторов

файл main.pu

    import data_download as dd  # импорт из файла data_download результатов работы функций
    import data_plotting as dplt  # импорт из файла data_plotting результатов работы функций

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

    # Вычисление технических индексов RSI и MACD
    # Функции calculate_rsi и calculate_macd файл data_download
    stock_data = dd.calculate_rsi(stock_data, window=14)
    stock_data = dd.calculate_macd(stock_data, fast_window=12, slow_window=26, signal_window=9)

    # Построим график данных
    dplt.create_and_save_plot(stock_data, ticker, period)


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


    def calculate_rsi(data, window=14):
    """Вычисляет технический индекс RSI(Relative Strength Index, индекс относительной силы) - показывающий
    соотношение положительных и отрицательных изменений цены финансового инструмента. Показывает, перекуплены(продавай)
    или перепроданы(покупай) акции.
    Определяет абсолютный прирост и падение цен за заданный период, а затем отношение между ними. Индикатор изменяется
    в диапазоне от 0 до 100. Если RSI<30 - акции перекуплены(продавай), если RSI>70 - акции перепроданы(покупай)
    Получает DataFrame с данными за указанный период и дополнительным столбцом Moving_Average и период для расчета RSI
    (по умолчанию стандартный 14-дневный)
    """
    # Вычисляем разницу между последовательными ценами закрытия
    diff = data['Close'].diff()  # вычисляем разницу между последовательными элементами данных колонки Close, DataFrame(метод diff())

    # Разделяем прибыли (положительные разницы) и убытки (отрицательные разницы)
    gain = diff.where(diff > 0, 0)  # Получить положительные разницы в качестве прироста(прибыль)
    loss = -diff.where(diff < 0, 0)  # Отрицательные разницы считаются потерями(убытки)

    # Рассчитываем средние прибыли и убытки, используя скользящее окно
    avg_gain = gain.rolling(window=window).mean()  # Рассчитать средний прирост(прибыль)
    avg_loss = loss.rolling(window=window).mean()  # Рассчитать средние потери(убытки)

    # Рассчитываем относительную силу (RS) путем деления средней прибыли на средние потери.
    rs = avg_gain / avg_loss

    # Рассчитываем RSI
    rsi = 100 - (100 / (1 + rs))

    # Добавляем рассчитанные значения RSI в качестве нового столбца в наборе данных
    data['RSI'] = rsi
    return data


    def calculate_macd(data, fast_window=12, slow_window=26, signal_window=9):
    """Вычисляет технический индекс MACD(индикатор схождения-расхождения скользящих средних) - служит индикатором
    импульса, который может сигнализировать о смене рыночного импульса и о потенциальных пробоях, помогает определить,
    когда рынок становится перекупленным (пора продавать) или перепроданным (пора покупать).
    В основе расчёта индекса MACD лежит значение экспоненциального скользящего среднего(EMA), полученные за разные периоды.
    Получает DataFrame с данными за указанный период и дополнительным столбцом Moving_Average, период быстрой ЕМА равный
    12 дням, период медленной ЕМА равный 26 дням и период сигнальной линии равный 9 дням.
    """
    fast_ema = data['Close'].ewm(span=fast_window, adjust=False).mean()  # Рассчитываем быстрый ЕМА
    # Функция ewm() в Pandas вычисляет экспоненциально взвешенную скользящую среднюю для определённого числа предыдущих
    # периодов. Аргумент span (необязательно): определяет затухание в терминах диапазона. Аргумент alpha (необязательно):
    # определяет коэффициент сглаживания напрямую.
    slow_ema = data['Close'].ewm(span=slow_window, adjust=False).mean()  # Рассчитываем медленный ЕМА
    macd = fast_ema - slow_ema  # Рассчитываем индекс MACD
    signal = macd.ewm(span=signal_window, adjust=False).mean()  # Рассчитываем 9-дневный ЕМА, для сигнальной линии

    # Добавляем рассчитанные значения MACD и Signal(сигнальная линия) в качестве новых столбцов в наборе данных
    data['MACD'] = macd
    data['Signal'] = signal
    return data

файл data_download.pu

    import matplotlib.pyplot as plt  # импортируем модуль pyplot из библиотеки Matplotlib под псевдонимом plt
    import pandas as pd
    
    
    def create_and_save_plot(data, ticker, period, filename=None):
    """
    Создает и сохраняет график цены акций, скользящего среднего, RSI, MACD и стандартного отклонения.
    Получает - data: DataFrame с историческими данными; ticker: Символ акции; period: Период данных; filename: Имя файла
    для сохранения графика.
    """
    plt.figure(figsize=(20, 15))  # устанавливаем размер фигуры в дюймах
    # График цены и скользящего среднего
    plt.subplot(4, 1, 1)  # создаём график с четырьмя строками, одним столбцом и первым индексом
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):  # проверяем, является ли индекс данных типом datetime64
            dates = data.index.to_numpy()  # преобразуем индекс данных в массив NumPy
            plt.plot(dates, data['Close'].values, label='Цена закрытия')  # создаём график с ценами закрытия по
            # полученным датам
            plt.plot(dates, data['Moving_Average'].values, label='Скользящая средняя')  # создаём график
            # временного ряда со скользящим средним
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):  # если данные столбца «Дата» в фрейме данных
            # не являются типом данных datetime64
            data['Date'] = pd.to_datetime(data['Date'])  # столбец «Дата» в фрейме данных преобразуется в
            # формат datetime
        plt.plot(data['Date'], data['Close'], label='Цена закрытия')
        plt.plot(data['Date'], data['Moving_Average'], label='Скользящая средняя')

    plt.title(f"{ticker} Цена акций с течением времени")  # назначаем название графика
    plt.xlabel("Дата")  # ось X на графике будет обозначать дату
    plt.ylabel("Цена")  # ось Y на графике будет обозначать цену
    plt.legend()  # добавляем легенду в график

    # График RSI
    plt.subplot(4, 1, 2)  # создаём график с четырьмя строками, одним столбцом и вторым индексом
    if 'RSI' in data.columns:  # если в данных есть колонка с названием «RSI»
        plt.plot(data.index, data['RSI'], label='RSI')  # визуализация графика индикатора относительной силы (RSI)
        plt.axhline(y=70, color='r', linestyle='--', label='Покупай')  # добавление красной пунктирной горизонтальной
        # линии на высоте y=70 - "Покупай"
        plt.axhline(y=30, color='g', linestyle='--', label='Продавай')  # добавление зелёной пунктирной горизонтальной
        # линии на высоте y=30 - "Продавай"
        plt.title('Индекс относительной силы (RSI)')
        plt.xlabel("Дата")
        plt.ylabel("RSI")
        plt.legend()
    else:
        print("Столбец 'RSI' отсутствует в данных.")

    # График MACD
    plt.subplot(4, 1, 3)  # создаём график с четырьмя строками, одним столбцом и третьим индексом
    if 'MACD' in data.columns and 'Signal' in data.columns:  # если в данных есть колонка с названием «MACD» и «Signal»
        plt.plot(data.index, data['MACD'], label='MACD')  # визуализация графика индикатора схождения-расхождения
        # скользящих средних (MACD)
        plt.plot(data.index, data['Signal'], label='Signal')  # визуализация графика сигнальной линии(Signal)
        plt.title('Конвергенция - Дивергенция скользящей средней (MACD)')
        plt.xlabel("Дата")
        plt.ylabel("MACD")
        plt.legend()
    else:
        print("Столбцы 'MACD' или 'Signal' отсутствуют в данных.")

    if filename is None:  # если имя файла не определено
        filename = f"{ticker}_{period}_stock_price_chart.png"  # имя файла принять "символ акции"_"период данных"
        # _stock_price_chart.png

    plt.savefig(filename)  # сохранение созданной фигуры, в файл с именем «filename.png».
    print(f"График сохранен как {filename}")
![2024-12-18_09-37-10.png](..%2F..%2F..%2FUsers%2FUser%2FDownloads%2F2024-12-18_09-37-10.png)
![2024-12-18_09-37-42.png](..%2F..%2F..%2FUsers%2FUser%2FDownloads%2F2024-12-18_09-37-42.png)
![2024-12-18_09-38-06.png](..%2F..%2F..%2FUsers%2FUser%2FDownloads%2F2024-12-18_09-38-06.png)
![2024-12-18_09-35-54.png](..%2F..%2F..%2FUsers%2FUser%2FDownloads%2F2024-12-18_09-35-54.png)


