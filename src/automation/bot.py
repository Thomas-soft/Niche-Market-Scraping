import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.console import console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from utils.cookies import refuse_cookies
from utils.errors import element_not_found_error
from data.save_to_csv import save_results, save_all_infos
from .scraping import get_sites, scrape_site
import json
import csv
from config.console import console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn


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
    driver.get(search_query)
    time.sleep(1)
    refuse_cookies(driver)
    time.sleep(1)
    sites = get_sites(driver, number_of_sites)
    save_results(sites, filename=file_to_save)


def run_bot2(driver, data, save_to_file):
    """
    Main function to run the bot.

    Args:
        driver: WebDriver
            The Selenium WebDriver.
        data: str
            Path to a CSV file containing the sites (first column).
        save_to_file: bool
            If True, the results will be saved to a CSV file.
    """
    # Lecture des sites depuis un fichier CSV
    if data.endswith(".csv"):
        with open(data, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            sites = [row[0] for row in reader]
    else:
        # Si 'data' n'est pas un fichier CSV, on suppose qu'il s'agit d'une liste de sites
        sites = data

    # Supposons que la première ligne est un header si elle ne commence pas par "http"
    urls = sites[1:] if sites and not sites[0].startswith("http") else sites

    # Remplacez par votre vraie clé API SimilarWeb
    API_KEY_SIMILARWEB = "YOUR_API_KEY_HERE"
    results = []

    # Affichage d'une barre de chargement avec l'URL en cours
    with Progress(
         SpinnerColumn(),
         TextColumn("[bold blue]{task.description}"),
         BarColumn(),
         TextColumn("{task.completed}/{task.total}"),
         TextColumn("[cyan]{task.fields[url]}"),
         console=console,
         transient=True  # La barre disparaît à la fin
    ) as progress:
         task = progress.add_task("Scraping sites...", total=len(urls), url="Starting...")
         for site in urls:
             # Met à jour la barre avec l'URL actuelle
             progress.update(task, description="Scraping", url=f"{site}")
             # Appelle votre fonction de scraping pour ce site (à adapter selon votre code)
             result = scrape_site(driver, site, API_KEY_SIMILARWEB)
             results.append(result)
             progress.advance(task)

    # Sauvegarde les résultats dans un fichier CSV
    if save_to_file:
        save_all_infos(results, filename="output/all_data.csv")

