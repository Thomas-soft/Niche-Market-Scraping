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
from automation.scraping import get_sites


def run_bot(driver, search_query, number_of_sites):
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
    save_results(sites, filename="output/data.csv")
    finished_info()
