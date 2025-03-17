import requests
from config.console import console


def get_current_location():
    """
    Get the current location of the user.

    return:
        latitude : float : The latitude of the user.
        longitude : float : The longitude of the user.
    """
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        if data["status"] == "success":
            return data.get("lat"), data.get("lon")
        else:
            console.print(f"[red]Erreur géolocalisation : {data.get('message')}[/red]")
            return None, None
    except Exception as e:
        console.print(f"[red]Erreur lors de la récupération de la géolocalisation: {e}[/red]")
        return None, None


def set_geolocation(driver, latitude, longitude, accuracy=100):
    """
    Configure the geolocation of the WebDriver.

    args:
        driver : WebDriver : The WebDriver object to navigate the web.
        latitude : float : The latitude of the location to set.
        longitude : float : The longitude of the location to set.
        accuracy : int : The accuracy of the location in meters.
    """
    driver.execute_cdp_cmd("Emulation.setGeolocationOverride", {
        "latitude": latitude,
        "longitude": longitude,
        "accuracy": accuracy
    })
