import time
from config.console import console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from utils.output import welcome_message, finished_info


def run_bot(driver, search_query, number_of_sites):

    """
    Main function to run the bot.

    args:
        driver : WebDriver : The WebDriver object to navigate the web.
        search_query : str : The search query to be used on Google.
        number_of_sites : int : The number of sites to scrape.
    """

    # Vérifie si search_query ressemble à une URL, sinon on construit une URL de recherche Google.
    if not search_query.startswith("http"):
        search_query = f"https://www.google.com/search?q={search_query}"

    welcome_message(search_query, number_of_sites)
    
    # Lancement de la navigation vers l'URL de recherche
    driver.get(search_query)
    
    # Simulation d'un processus de scraping avec une barre de progression
    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TextColumn("{task.completed} of {task.total} scraped sites"),
        console=console,
    ) as progress:
        task = progress.add_task("Scraping...", total=number_of_sites)
        for _ in range(number_of_sites):
            # Ici, vous insérerez votre code de scraping pour chaque site.
            # La ligne suivante simule le temps nécessaire à la récupération d'un site.
            time.sleep(1)
            progress.update(task, advance=1)
    
    finished_info()
