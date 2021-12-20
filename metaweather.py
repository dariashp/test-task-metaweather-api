import datetime
from urllib.parse import urljoin

import requests

METAWEATHER_URL = "https://www.metaweather.com/"
RAIN_ABBREVIATIONS = ("h", "t", "hr", "lr", "s")

INVALID_CITY_MSG = "Invalid city name"
NO_CITY_FORECAST_MSG = "No forecast for the given city"
GONNA_RAIN_MSG = "It's going to rain tomorrow"
NOT_GONNA_RAIN_MSG = "There will be no rain tomorrow"


def send_request(url, payload=None):
    """Send request to metaweather api. Return value depends on endpoint's return value"""
    request_url = urljoin(METAWEATHER_URL, url)
    response = requests.get(request_url, params=payload)
    return response.json()


def get_city_id(city):
    """Retrieve city's id. Return str"""
    url = "/api/location/search/"
    payload = {"query": city}
    response = send_request(url, payload)
    if not response:
        return None
    return response[0].get("woeid")


def get_city_forecast(woeid):
    """Retrieve city's weather. Return Dict"""
    url = f"/api/location/{woeid}/"
    response = send_request(url)
    return response.get("consolidated_weather")


def get_city_forecast_for_date(woeid, date):
    """Retrieve city's weather on specific date. Return List"""
    url = f"/api/location/{woeid}/{date}"
    response = send_request(url)
    return response


def get_tomorrow_forecast(woeid, day):
    """Send request to retrieve weather for given city. Filter forecast by date. Return str or Dict"""
    weather = get_city_forecast(woeid)
    if not weather:
        return NO_CITY_FORECAST_MSG

    tomorrow_forecast = tuple(filter(lambda x: x["applicable_date"] == day.strftime("%Y-%m-%d"), weather))[0]
    return tomorrow_forecast


def get_tomorrow_forecast_based_on_predictability(woeid, day):
    """Send request to retrieve weather on the given date.
    Select forecast with highest predictability. Return str or Dict"""
    tomorrow_string = day.strftime("%Y/%m/%d")
    weather = get_city_forecast_for_date(woeid, tomorrow_string)
    if len(weather) == 0:
        return NO_CITY_FORECAST_MSG

    # take forecast that has the biggest predictability value
    tomorrow_forecast = sorted(weather, key=lambda x: x["predictability"], reverse=True)[0]
    return tomorrow_forecast


def check_for_rain(tomorrow_forecast):
    """Check if it's gonna rain. Return bool"""
    is_raining = tomorrow_forecast["weather_state_abbr"] in RAIN_ABBREVIATIONS
    return is_raining


def get_forecast_for_tomorrow(city):
    """Get forecast for given city. Return str"""
    woeid = get_city_id(city)
    if not woeid:
        return INVALID_CITY_MSG

    tomorrow = datetime.date.today() + datetime.timedelta(days=1)
    # Here either get_tomorrow_forecast() or get_tomorrow_forecast_based_on_predictability() can be used.
    # Just uncomment the one you want to use. The difference is in the api endpoint each function uses

    # tomorrow_forecast = get_tomorrow_forecast(woeid, tomorrow)
    tomorrow_forecast = get_tomorrow_forecast_based_on_predictability(woeid, tomorrow)
    if type(tomorrow_forecast) == str:
        return tomorrow_forecast

    is_raining = check_for_rain(tomorrow_forecast)
    forecast = GONNA_RAIN_MSG if is_raining else NOT_GONNA_RAIN_MSG
    return forecast
