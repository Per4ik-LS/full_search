import requests
def get_coordinates(address: str) -> tuple[float, float]:
    ...


API_KEY = "40d1649f-0493-4b70-98ba-98533de7710b"

def geocoder_request(address: str) -> dict:
    response = requests.get("http://geocode-maps.yandex.ru/1.x/", params={
        "apikey": API_KEY,
        "geocode": address,
        "format": "json",
    })

    if not response:
        raise RuntimeError(
            f'''Ошибка выполнения запроса:
            {geocoder_request}
            Http статус {response.status_code} ({response.reason})''')
    data = response.json()

    features = data["response"]["GeoObjectCollection"]["featureMember"]
    return features[0]["GeoObject"] if features else None