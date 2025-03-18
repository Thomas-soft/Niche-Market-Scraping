from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from utils.errors import element_not_found_error
from config.console import console


def get_sites(driver, number_of_sites):
    sites = []
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

    # remove any non-URL and remove all after the first space
    sites = [site.split(" ")[0] for site in sites if site[:4] == "http"]
    console.print(Panel("\n".join(sites), title="Found Sites", expand=False))
    return sites
