from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from config.console import console
from utils.localisation import get_current_location, set_geolocation
import sys


def create_instance(headless=False):
    """
    Create a new instance of the WebDriver.
    """
    options = uc.ChromeOptions()
    if headless:
        options.add_argument("--headless")           # Mode headless pour ne pas afficher le navigateur
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
    else:
        options.add_argument("--start-maximized")
    driver = None
    if sys.platform != "Darwin":
        driver = uc.Chrome(options=options)
    else:
        driver = uc.Chrome(driver_executable_path=ChromeDriverManager().install(), options=options)
    return driver


def configure_geolocation(driver, latitude, longitude, accuracy=100):
    """
    Configure the geolocation of the WebDriver.
    """
    if latitude is not None and longitude is not None:
        set_geolocation(driver, latitude, longitude, accuracy)
        console.print(f"Géolocalisation fixée sur : Latitude {latitude}, Longitude {longitude}")
    else:
        lat, lon = get_current_location()
        if lat is not None and lon is not None:
            set_geolocation(driver, lat, lon)
            console.print(f"Géolocalisation auto-détectée : Latitude {lat}, Longitude {lon}")
        else:
            console.print("[red]Impossible de récupérer la géolocalisation automatique, la position par défaut sera utilisée.[/red]")
