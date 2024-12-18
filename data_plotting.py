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
    print(f"График сохранен {filename}")









