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


# Запуск процесса
if __name__ == "__main__":
    main()
