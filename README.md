# Анализ и визуализации данных об акциях

    import data_download as dd  # импорт из файла data_download результатов работы функций
    import data_plotting as dplt  # импорт из файла data_plotting результатов работы функций

## def main():
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

    # Получение данных о запасах, функция fetch_stock_data файл data_download
    period = input("введите период или пропустить(ENTER) для ввода конкретных дат:»")
    if not period:
        start_date = input("Введите дату начала анализа в формате 'ГГГГ-ММ-ДД' (например, '2022-01-01'): ")
        end_date = input("Введите дату окончания анализа в формате 'ГГГГ-ММ-ДД' (например, '2022-12-31'): ")
        stock_data = dd.fetch_stock_data(ticker, start_date=start_date, end_date=end_date)
    else:
        stock_data = dd.fetch_stock_data(ticker, period=period)

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

    # Добавление технических индексов RSI и MACD
    # Функции calculate_rsi и calculate_macd файл data_download
    stock_data = dd.calculate_rsi(stock_data, window=14)
    stock_data = dd.calculate_macd(stock_data, fast_window=12, slow_window=26, signal_window=9)

    # добавление статистического показателя - стандартное отклонение цены акции
    # Функции calculate_std_dev файл data_download
    stock_data = dd.calculate_std_dev(stock_data)

    # Построим график данных акций
    # Функции create_and_save_plot файл data_plotting
    # Пользователь назначает стиль оформление графика
    style = input("введите пропустить(ENTER) для создания графика в стиле classic(по умолчанию)"
                  "или скопируйте или введите вручную названия стиля графика: \n"
                  "default - (белый лист, белый фон графика, сетки нет, чёрные буквы и цифры одинаковых размеров);\n"
                  "Solarize_Light2 - (кремовый лист, серый фон графика, белая сетка, серый буквы и цифры графика, "
                  "чёрные буквы названий) ;\n"
                  "bmh - (белый лист, серый фон графика, серая сетка, чёрные буквы и цифры разных размеров);\n"
                  "dark_background - (чёрный лист, фон графика чёрный, сетки нет, а цвет тиков — белый.):»\n")
    if not style:
        style = 'classic'
    dplt.create_and_save_plot(stock_data, ticker, period, style=style)
    dplt.create_interactive_graphs(stock_data, ticker, period)

    # Запуск процесса
    if __name__ == "__main__":
        main()

## файл data_download.pu

    import yfinance as yf  # импорт библиотеки yfinance с использованием псевдонима yf - предоставляет доступ к финансовым
    # данным из Yahoo Finance.
    """test
    import pandas as pd  # импорт библиотеки Pandas - мощный инструмент для анализа и обработки табличных данных
    (pd- общепринятое сокращение для Pandas в коде)
    from tabulate import tabulate  # test - импорт библиотеки tabulate - красивое оформление таблицы
    """


    def fetch_stock_data(ticker, period=None, start_date=None, end_date=None):
    """Получает исторические данные об акциях для указанного тикера и временного периода. Возвращает DataFrame с данными.
    Тикер — это краткое название в биржевой информации котируемых инструментов (акций, облигаций, индексов).
    Является уникальным идентификатором в рамках одной биржи или информационной системы. Используется для того,
    чтобы постоянно не печатать в сводках полное наименование ценных бумаг или других объектов торговли.
    DataFrame - структура хранения данных, организованных в двух изменениях(строках и столбцах)
    и соответствующих этим строкам и столбцам меток """
    data = None
    stock = yf.Ticker(ticker)  # создаём объект модуля Ticker с заданным тикером.
    # Модуль Ticker позволяет получить список последних финансовых новостей по заданному тикеру.
    if period:
        data = stock.history(period=period)  # получаем исторические данные об акциях для указанного тикера и
        # временного периода.
    elif start_date and end_date:
        data = stock.history(start=start_date, end=end_date)  # получаем исторические данные об акциях
        # для указанного тикера и временного периода в указанном диапазоне дат.
    return data


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
    """test
    df = pd.read_csv('dataframe.csv')  # читаем CSV файл(функция read_csv) с названием dataframe
    headers = ['№', 'Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Dividends', 'Stock Splits', 'Moving_Average']
    # назначаем название столбцов
    print('************************ПОЛУЧЕННЫЕ ДАННЫЕ ОБ АКЦИЯХ************************')
    print(tabulate(df, headers=headers, tablefmt='grid', stralign='center'))  # выводим в консоль,
    # сохранённую DataFrame из CSV файл с названием dataframe
    """


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
    # print(data)  # test
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
    # print(data)  # test
    return data

    def calculate_std_dev(data):
    """Вычисляет статистический показатель - стандартное отклонение цены акции - этот показатель количественно определяет
    разброс цен активов относительно их среднего значения и дает представление об изменчивости и потенциальном риске,
    связанном с финансовым инструментом. Более высокое стандартное отклонение указывает на большую изменчивость цен и
    более значительные колебания, а более низкое значение указывает на меньшие колебания цен.
    Принимает DataFrame с данными за указанный период и дополнительным столбцом Moving_Average.
    #test
    list_prices_close = data['Close'].tolist() # сбор данных о ценах закрытия акции за указанный период(в список)
    n = len(list_prices_close) # сохраняем длину списка в переменную п
    average = sum(list_prices_close) / n # сохраняем среднее значение полученных данных в переменную average
    var = sum((i-average)**2 for i in list_prices_close) / (n - 1) # определяем и сохраняем дисперсию цен в переменную
    var(сумма всех значений квадратов отклонений(разница значения каждой цены закрытия и среднего значения разделённое
    на количество цен минус одна (эта корректировка, известная как поправка Бесселя, используется для выборки))
    std_dev = var ** 0.5 # определяем стандартное отклонение цены акции(корень квадратный из дисперсии цен)
    data['Standard Deviation'] = std_dev
    """
    data['std_deviation'] = data['Close'].std()  # определяем стандартное отклонение цены акции(std_dev) с помощью функции
    # pandas - DataFrame.std() и сохраняем данные в DataFrame
    # print(data.to_string()) # test - выводим в консоль DataFrame со всеми столбцами
    return data

## файл data_plotting.pu

    import matplotlib.pyplot as plt  # импортируем модуль pyplot из библиотеки Matplotlib под псевдонимом plt
    import pandas as pd
    import matplotlib.dates as mdates  # импорт модуля для работы с датами в библиотеке Matplotlib
    from bokeh.plotting import figure, show, output_file  # импорт функций библиотеки Bokeh
    
    
    def create_and_save_plot(data, ticker, period, filename=None, style='style'):
    """
    Создает и сохраняет график цены акций, скользящего среднего, RSI, MACD и стандартного отклонения.
    Получает - data: DataFrame с историческими данными и дополнительным столбцом Moving_Average; ticker: Символ акции;
    period: Период данных; filename: Имя файла для сохранения графика; стиль графика - не определён.
    """
    plt.style.use(style)  # назначаем стиль оформления графика, указанный пользователем
    plt.figure(figsize=(20, 12))  # устанавливаем размер фигуры в дюймах
    # График цены и скользящего среднего
    plt.subplot(4, 1, 1)  # создаём график с четырьмя строками, одним столбцом и первым индексом
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):  # проверяем, является ли индекс данных типом datetime64
            dates = data.index.to_numpy()  # преобразуем индекс данных в массив NumPy
            plt.plot(dates, data['Close'].values, alpha=1, label='Цена закрытия')  # создаём график с ценами закрытия по
            # полученным датам
            plt.plot(dates, data['Moving_Average'].values, alpha=1, label='Скользящая средняя')  # создаём график
            # временного ряда со скользящим средним
            plt.plot(dates, data['Moving_Average'] - 2 * data['std_deviation'], data['Moving_Average'] +
                     2 * data['std_deviation'], color='c', alpha=0.5, label='Стандартное отклонение')
            # создаём полосы Боллинджера (график стандартного отклонения)
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):  # если данные столбца «Дата» в фрейме данных
            # не являются типом данных datetime64
            data['Date'] = pd.to_datetime(data['Date'])  # столбец «Дата» в фрейме данных преобразуется в
            # формат datetime
        plt.plot(data['Date'], data['Close'], alpha=1, label='Цена закрытия')
        plt.plot(data['Date'], data['Moving_Average'], alpha=1, label='Скользящая средняя')
        plt.plot(data['Date'], data['Moving_Average'] - 2 * data['std_deviation'], data['Moving_Average'] +
                 2 * data['std_deviation'], color='c', alpha=0.5, label='Стандартное отклонение')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%y"))  # меняем формат даты по оси Х на ДД.ММ.ГГ
    plt.title(f"{ticker} Цена акций с течением времени")  # назначаем название графика
    plt.xlabel("Дата")  # ось X на графике будет обозначать дату
    plt.ylabel("Цена")  # ось Y на графике будет обозначать цену
    plt.legend()  # добавляем легенду в график
    plt.subplots_adjust(hspace=0.5)  # делаем отступ от графика

    # График RSI
    plt.subplot(4, 1, 2)  # создаём график с четырьмя строками, одним столбцом и вторым индексом
    if 'RSI' in data.columns:  # если в данных есть колонка с названием «RSI»
        plt.plot(data.index, data['RSI'], label='RSI')  # визуализация графика индикатора относительной силы (RSI)
        plt.axhline(y=70, color='r', linestyle='--', label='Покупай')  # добавление красной пунктирной горизонтальной
        # линии на высоте y=70 - "Покупай"
        plt.axhline(y=30, color='g', linestyle='--', label='Продавай')  # добавление зелёной пунктирной горизонтальной
        # линии на высоте y=30 - "Продавай"
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%y"))
        plt.title('Индекс относительной силы (RSI)')
        plt.xlabel("Дата")
        plt.ylabel("RSI")
        plt.legend()
        plt.subplots_adjust(hspace=0.5)
    else:
        print("Столбец 'RSI' отсутствует в данных.")

    # График MACD
    plt.subplot(4, 1, 3)  # создаём график с четырьмя строками, одним столбцом и третьим индексом
    if 'MACD' in data.columns and 'Signal' in data.columns:  # если в данных есть колонка с названием «MACD» и «Signal»
        plt.plot(data.index, data['MACD'], label='MACD')  # визуализация графика индикатора схождения-расхождения
        # скользящих средних (MACD)
        plt.plot(data.index, data['Signal'], label='Signal')  # визуализация графика сигнальной линии(Signal)
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%d.%m.%y"))
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
    print(f"График сохранен {filename}")


    def create_interactive_graphs(data, ticker, period=None):
    average_price = data['Close'].mean(axis=0)  # Вычисляем среднее значение строк столбца Close
    # Добавление сюжета
    p = figure(width=1800, height=900, title=f'{ticker} Цена акций с течением времени', x_axis_type='datetime',
               x_axis_label='Дата', y_axis_label='Цена')
    x = []
    y = []
    # Данные для графика
    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):  # проверяем, является ли индекс данных типом datetime64
            dates = data.index.to_numpy()  # преобразуем индекс данных в массив NumPy
            x = dates
            y = data['Close'].tolist()
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):  # если данные столбца «Дата» в фрейме данных
            # не являются типом данных datetime64
            dates = pd.to_datetime(data['Date'])  # столбец «Дата» в фрейме данных преобразуется в
            # формат datetime
            x = dates
            y = data['Close'].tolist()
    # Добавление линии на график
    p.line(x, y, legend_label="Цена закрытия", line_width=1.5)
    p.circle(x, y, fill_color='white', size=5)
    p.title.text_font_size = '25px'
    p.title.text_font = "arial"
    p.title.align = "center"
    # Определение выходного файла
    output_file('index.html')
    print(f'СРЕДНЯЯ ЦЕНА ЗАКРЫТИЯ АКЦИЙ ЗА ЗАДАННЫЙ ПЕРИОД:":  {average_price}\n')
    print(f"Создан интерактивный график {ticker} - цена акций с течением времени")
    # Отображение результатов
    show(p)
![2024-12-26_10-59-27](https://github.com/user-attachments/assets/f85a1614-8522-411f-bda1-bd9ad15e6814)
![2024-12-26_11-00-31](https://github.com/user-attachments/assets/b7998dbb-16a4-42fe-8afe-60686304aadf)
![2024-12-26_10-58-22](https://github.com/user-attachments/assets/d5a62acc-8c31-46b5-842f-394035eb8642)
![2024-12-27_12-29-22](https://github.com/user-attachments/assets/fb7de475-9528-436f-974b-57eca633b9f7)




