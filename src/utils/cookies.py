import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from config.console import console


def refuse_cookies(driver):
    """
    Attempts to decline cookies by clicking on a cookie refusal button.
    Waits up to 10 seconds for a button to become clickable. If none is found,
    it waits an additional 10 seconds and logs an error.
    """
    
    try:
        button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Reject all') and @role='none']"))
        )
        button.rect['height'] = 10
        button.rect['width'] = 10
        button.click()
        console.print("[green]✅ Cookies have been declined.[/green]")
    except TimeoutException:
        console.print("[yellow]❌ No cookie decline button found after waiting 10 seconds.[/yellow]")
