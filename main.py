from metaweather import get_forecast_for_tomorrow


def main():
    entered_city = input("Enter city name: ")
    try:
        forecast = get_forecast_for_tomorrow(entered_city)
        print(forecast)
    except (ConnectionError, ValueError) as e:
        print(e)


if __name__ == "__main__":
    main()
