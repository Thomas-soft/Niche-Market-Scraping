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
    sites = []  # List to store the found sites
    time.sleep(5)  # Wait for the page to load
    with Progress(
        SpinnerColumn(),
        "[progress.description]{task.description}",
        BarColumn(),
        TextColumn("{task.completed} out of {task.total} sites found"),
        console=console,
    ) as progress:
        task = progress.add_task("Collecting sites", total=number_of_sites)
        
        while len(sites) < number_of_sites:
            try:
                # Wait up to 10 seconds for the <cite> elements with role="text" to appear
                cite_elements = WebDriverWait(driver, 10).until(
                    lambda d: d.find_elements(By.XPATH, "//cite[@role='text']")
                )
            except TimeoutException as e:
                element_not_found_error(f"No cite elements found after waiting 10 seconds: {e}")

            for elem in cite_elements:
                site_text = elem.text.strip()
                if site_text and site_text not in sites:
                    sites.append(site_text)
                    progress.update(task, advance=1)
                    if len(sites) >= number_of_sites:
                        break

            if len(sites) < number_of_sites:
                try:
                    # Wait up to 10 seconds for the "Next" button to be clickable
                    next_button = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable((By.ID, "pnnext"))
                    )
                    next_button.rect['height'] = 10
                    next_button.rect['width'] = 10
                    next_button.click()
                except TimeoutException as e:
                    element_not_found_error(f"Unable to navigate to the next page after waiting 10 seconds: {e}")

    console.print(Panel("\n".join(sites), title="Found Sites", expand=False))

    # Save the results to a CSV file
    save_results(sites, filename="data.csv")

    finished_info()
