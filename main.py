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


# Запуск процесса
if __name__ == "__main__":
    main()
