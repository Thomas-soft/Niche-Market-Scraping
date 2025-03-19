import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.console import console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from utils.output import welcome_message, finished_info
from utils.cookies import refuse_cookies
from utils.errors import element_not_found_error
from data.save_to_csv import save_results
from .scraping import get_sites, scrape_site
import json


def run_bot1(driver, search_query, number_of_sites, file_to_save):
    """
    Main function to run the bot.
    
    Args:
        driver: WebDriver
            The WebDriver object to navigate the web.
        search_query: str
            The search query to be used on Google.
        number_of_sites: int
            The number of sites to list.
    """
    # If search_query is not a URL, build a Google search URL.
    if not search_query.startswith("http"):
        search_query = f"https://www.google.com/search?q={search_query}"
    welcome_message(search_query, number_of_sites)
    driver.get(search_query)
    refuse_cookies(driver)
    sites = get_sites(driver, number_of_sites)
    save_results(sites, filename=file_to_save)
    finished_info()


def run_bot2(driver, data, save_to_file):
    sites = [
        "https://www.alexandrecoiffure-lh.fr",
        "https://www.salon-bemyme.com",
        "https://salons.coiffandco.com/fr/coiffeur/"
    ]
    # Remplacez par votre vraie clé API SimilarWeb
    API_KEY_SIMILARWEB = "YOUR_API_KEY_HERE"
    results = []
    for site in sites:
        print(f"Scraping {site} ...")
        result = scrape_site(driver, site, API_KEY_SIMILARWEB)
        results.append(result)
    print(json.dumps(results, indent=4, ensure_ascii=False))
