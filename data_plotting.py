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

