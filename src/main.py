import os
import sys
from config.console import console
from rich.panel import Panel
from automation.bot import run_bot1, run_bot2
from utils.output import bot_configuration_info
import utils.errors as error
from utils.check_args import check_args
from config.bot import create_instance, configure_geolocation


def main(search_query, number_of_sites, latitude=None, longitude=None):

    """
    Main function to run the bot.

    The bot will scrape the first n websites from a Google search query.

    args:
        search_query : str : The search query to be used on Google.
        number_of_sites : int : The number of sites to scrape.
        latitude (optional) : float : The latitude of the location to search from.
        longitude (optional) : float : The longitude of the location to search
    """

    # Lancement du bot (fonction importée)
    bot_configuration_info(search_query, number_of_sites)
    # Configuration du webdriver
    driver = create_instance(headless=False)
    # Gestion de la géolocalisation
    configure_geolocation(driver, latitude, longitude)
    run_bot1(driver, search_query, number_of_sites, file_to_save="output/data.csv")
    driver.quit()
    driver = create_instance(headless=True)
    run_bot2(driver, data="output/data.csv", save_to_file="output/database.csv")
    driver.quit()
    console.print(Panel("Bot finished", title="Bot", expand=False))


if __name__ == "__main__":
    args = sys.argv
    argv, argc, latitude, longitude = check_args(args)
    main(argv, argc, latitude, longitude)
    sys.exit(0)
