import json


from metaweather import (
    METAWEATHER_URL,
    get_city_id,
    get_city_forecast,
    get_city_forecast_for_date,
    check_for_rain,
)


def test_get_city_id(requests_mock):
    requests_mock.get(f"{METAWEATHER_URL}api/location/search/?query=London", json=[{"woeid": 44418}])
    city_id = get_city_id("London")
    assert city_id == 44418


def test_get_city_forecast(requests_mock):
    with open("test_data/city_forecast_data.json") as f:
        data = json.load(f)
        requests_mock.get(f"{METAWEATHER_URL}api/location/44418/", json=data)
    city_forecast = get_city_forecast(44418)
    assert city_forecast[0]["id"] == 5140502191013888
    assert city_forecast[0]["weather_state_abbr"] == "hc"
    assert len(city_forecast) == 6


def test_get_city_forecast_for_date(requests_mock):
    with open("test_data/city_forecast_for_date_data.json") as f:
        data = json.load(f)
        requests_mock.get(f"{METAWEATHER_URL}api/location/44418/2021/12/20/", json=data)
    date = "2021/12/20/"
    city_forecast = get_city_forecast_for_date(44418, date)
    assert city_forecast[0]["id"] == 5140502191013888
    assert len(city_forecast) == 3


def test_check_for_rain():
    forecast = {"id": 1, "weather_state_name": "Light Rain", "weather_state_abbr": "lr", "predictability": 71}
    is_raining = check_for_rain(forecast)
    assert is_raining is True


def test_check_for_rain_false():
    forecast = {"id": 1, "weather_state_name": "Clear", "weather_state_abbr": "c", "predictability": 71}
    is_raining = check_for_rain(forecast)
    assert is_raining is False


