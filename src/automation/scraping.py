from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn
from utils.errors import element_not_found_error
from config.console import console
from utils.urls import get_pages, get_domain_from_url
from Wappalyzer import Wappalyzer, WebPage
import json
import re
from bs4 import BeautifulSoup
import warnings
import time
from selenium.webdriver.support.ui import WebDriverWait


# Masquer l'avertissement de Wappalyzer sur la regex
warnings.filterwarnings("ignore", message="Caught 'unbalanced parenthesis")


def wait_for_dynamic_content(driver, timeout=20):
    """
    Wait until the page is fully loaded, including dynamic content.
    
    This function waits until:
      - document.readyState equals "complete"
      - If jQuery is available, jQuery.active is 0 (i.e. no ongoing AJAX requests)
      
    Args:
        driver: Selenium WebDriver instance.
        timeout: Maximum wait time in seconds.
    """
    
    # Wait for document.readyState to be "complete"
    WebDriverWait(driver, timeout).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    
    # If jQuery is present, wait for all AJAX requests to finish
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return (typeof jQuery != 'undefined') ? jQuery.active == 0 : true")
        )
    except Exception as e:
        print("Warning: jQuery wait not applicable or failed:", e)
        return False
    return True


def get_sites(driver, number_of_sites):
    sites = []
    if wait_for_dynamic_content(driver) is False:
        element_not_found_error("Page not fully loaded after waiting 20 seconds")
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
                    time.sleep(1)
                    next_button.click()
                except TimeoutException as e:
                    element_not_found_error(f"Unable to navigate to the next page after waiting 10 seconds: {e}")

    # remove any non-URL and remove all after the first space
    sites = [site.split(" ")[0] for site in sites if site[:4] == "http"]
    console.print(Panel("\n".join(sites), title="Found Sites", expand=False))
    return sites


def get_site_content(driver, site):
    """
    Get the content of a site
    tel, email, name of company, activity sector, trafic monthly, tools used (WordPress, Shopify, CraftCMS...), precence or no of pixel Facebook / Google Analytics / Tag Manager, ads activity detected  (Google Ads, Facebook Ads...)

    args:
        driver: selenium webdriver
        site: str, url of the site to scrape
    return:
        dict: site content
    """

    driver.get(site)


def extract_contacts(html):
    """
    Extrait les emails et numéros de téléphone à partir du HTML.
    - Pour les emails : recherche dans les liens "mailto:".
    - Pour les téléphones : recherche dans les liens "tel:" et dans le texte des balises <a>
      qui pourraient contenir un numéro au format français (ex: "02 35 41 14 40").
    """
    soup = BeautifulSoup(html, 'html.parser')
    emails = set()
    telephones = set()

    # Regex pour un numéro français : 0 suivi de 9 chiffres, éventuellement séparés par un espace, tiret ou point.
    phone_regex = re.compile(r'\b0\d(?:[\s.-]?\d{2}){4}\b')

    for a in soup.find_all('a', href=True):
        href = a['href']
        if href.startswith('mailto:'):
            # Extraction de l'email
            email_part = href.split('mailto:')[1].split('?')[0]
            for email in re.split(r'[;,]', email_part):
                email_clean = email.strip()
                if email_clean:
                    emails.add(email_clean)
        elif href.startswith('tel:'):
            # Extraction d'un numéro via le lien tel:
            phone = href.split('tel:')[1]
            phone = re.sub(r'[\s.-]', '', phone)
            telephones.add(phone)
        else:
            # Sinon, vérifier si le texte du lien contient un numéro de téléphone.
            link_text = a.get_text(separator=' ', strip=True)
            matches = phone_regex.findall(link_text)
            for match in matches:
                # Nettoyage des séparateurs pour obtenir un numéro compact
                clean_number = re.sub(r'[\s.-]', '', match)
                telephones.add(clean_number)
    
    return emails, telephones


def extract_cms(url):
    """
    Utilise Wappalyzer pour détecter l'outil utilisé (CMS) à partir de l'URL.
    Parcourt les technologies détectées et retourne le CMS s'il fait partie d'une liste connue.
    """
    # web_page = WebPage.new_from_url(url)
    # wappalyzer = Wappalyzer.latest()
    # tech_results = wappalyzer.analyze_with_categories(web_page)

    # tech_results = [name for name, details in tech_results.items() if 'CMS' in details.get('categories', [])]
    # if not tech_results:
    #     return "Unknown"
    # return tech_results[0]
    return "A implémenter"


def extract_company_info(html):
    """
    Essaie d'extraire le nom de l'entreprise et son secteur d'activité en utilisant plusieurs méthodes :

    1. JSON-LD : Recherche des scripts de type "application/ld+json" avec "@type": "Organization".
       On y cherche les clés "name" pour le nom et "industry" pour le secteur.
    2. Microdata : Recherche un élément avec itemtype "http://schema.org/Organization" et
       extrait les valeurs des attributs itemprop="name" et itemprop="industry".
    3. Balise Meta Open Graph : En dernier recours, on récupère le nom via la balise meta "og:site_name".
       Pour le secteur, il n'existe pas de meta standard, donc cette méthode ne concerne que le nom.

    Retourne un tuple (nom, secteur) ou (None, None) si rien n'est trouvé.
    """
    soup = BeautifulSoup(html, 'html.parser')
    company_name = None
    sector = None

    # 1. JSON-LD
    for script in soup.find_all('script', type='application/ld+json'):
        try:
            data = json.loads(script.string)
            if isinstance(data, list):
                for entry in data:
                    if entry.get('@type') == 'Organization':
                        company_name = entry.get('name')
                        sector = entry.get('industry')
                        break
            elif isinstance(data, dict):
                if data.get('@type') == 'Organization':
                    company_name = data.get('name')
                    sector = data.get('industry')
        except Exception:
            continue
        if company_name is not None:
            break

    # 2. Microdata
    if not company_name:
        org_tag = soup.find(attrs={"itemtype": "http://schema.org/Organization"})
        if org_tag:
            name_tag = org_tag.find(attrs={"itemprop": "name"})
            if name_tag:
                company_name = name_tag.get_text(strip=True)
            industry_tag = org_tag.find(attrs={"itemprop": "industry"})
            if industry_tag:
                sector = industry_tag.get_text(strip=True)

    # 3. Balise Meta Open Graph
    if not company_name:
        meta_site_name = soup.find("meta", property="og:site_name")
        if meta_site_name and meta_site_name.get("content"):
            company_name = meta_site_name["content"]

    return company_name, sector


def get_similarweb_rank(domain, api_key):
    """
    Stub pour récupérer le rang global via l'API SimilarWeb (endpoint SimilarRank).
    À implémenter si nécessaire.
    """
    return "A implémenter"


def extract_pixels(html):
    """
    Vérifie la présence des pixels de suivi :
    - Facebook Pixel (détecte 'fbq(' ou 'Facebook Pixel')
    - Google Analytics (détecte 'UA-', 'gtag(', ou un identifiant GA4 avec le pattern 'G-[A-Z0-9]{4,}')
    - Google Tag Manager (détecte 'GTM-')
    
    Retourne un dictionnaire indiquant True/False pour chaque pixel.
    """
    facebook_pixel = 'fbq(' in html or 'Facebook Pixel' in html
    google_analytics = ('UA-' in html) or ('gtag(' in html)
    if not google_analytics:
        ga4_pattern = re.compile(r'G-[A-Z0-9]{4,}', re.IGNORECASE)
        if ga4_pattern.search(html):
            google_analytics = True
    google_tag_manager = 'GTM-' in html

    return {
        "facebook_pixel": facebook_pixel,
        "google_analytics": google_analytics,
        "google_tag_manager": google_tag_manager
    }


def extract_ad_activity(html):
    """
    Détecte l'activité publicitaire en cherchant des indices dans le HTML.
    - Pour Google Ads : recherche 'adsbygoogle', 'googleadservices', 'doubleclick' et 'adservice.google.com'.
    - Pour Facebook Ads : recherche 'facebook.com/tr' et 'fbq('.
    - Pour d'autres réseaux (ex. Outbrain, Taboola) : recherche 'outbrain' ou 'taboola'.
    
    Retourne un dictionnaire indiquant True/False pour chaque type d'activité publicitaire.
    """
    google_ads = ('adsbygoogle' in html) or ('googleadservices' in html) or ('doubleclick' in html) or ('adservice.google.com' in html)
    facebook_ads = ('facebook.com/tr' in html) or ('fbq(' in html)
    other_ads = ('outbrain' in html.lower()) or ('taboola' in html.lower())
    
    return {
        "google_ads": google_ads,
        "facebook_ads": facebook_ads,
        "other": other_ads
    }


def scrape_site(driver, base_url, api_key):
    """
    Scrape a site based on its base URL.
    Retrieves data from the main, contact, and about pages.
    
    This function dynamically waits for the page to load its complete content,
    ensuring that dynamically loaded elements (like Facebook Ads, tracking scripts, etc.)
    are present.
    
    Args:
        driver: Selenium WebDriver instance.
        base_url: str, the base URL of the site to scrape.
        api_key: API key for SimilarWeb (or other services).
    
    Returns:
        dict: Extracted site content with keys:
            - base_url
            - emails
            - telephones
            - nom_entreprise (Company Name)
            - secteur (Sector)
            - rang_global (Global Rank)
            - outil_utilisé (CMS or tool used)
            - pixels (tracking pixels)
            - activite_publicitaire (advertising activity)
    """
    pages = get_pages(base_url)  # Cette fonction doit retourner un dictionnaire de pages à scraper
    
    combined_emails = set()
    combined_telephones = set()
    company_name = None
    sector = None
    combined_pixels = {"facebook_pixel": False, "google_analytics": False, "google_tag_manager": False}
    combined_ad_activity = {"google_ads": False, "facebook_ads": False, "other": False}
    
    # Pour chaque type de page (par exemple : main, contact, about)
    for page_type, url in pages.items():
        # Charger la page
        driver.get(url)
        # Attendre que la page soit entièrement chargée et que le contenu dynamique soit rendu
        if wait_for_dynamic_content(driver, timeout=20) is False:
            print(f"Timeout while waiting for {url} to load")
            continue
        
        try:
            html = driver.page_source
        except Exception as e:
            print(f"Error while retrieving {url} : {e}")
            continue

        # Extraction des contacts (emails et téléphones)
        emails, telephones = extract_contacts(html)
        combined_emails.update(emails)
        combined_telephones.update(telephones)
        
        # Extraction des informations sur l'entreprise
        if not company_name:
            name_temp, sector_temp = extract_company_info(html)
            if name_temp:
                company_name = name_temp
            if sector_temp:
                sector = sector_temp
        
        # Extraction des pixels et de l'activité publicitaire
        pixels = extract_pixels(html)
        for k, v in pixels.items():
            combined_pixels[k] = combined_pixels[k] or v
        
        ad_act = extract_ad_activity(html)
        for k, v in ad_act.items():
            combined_ad_activity[k] = combined_ad_activity[k] or v
    
    cms = extract_cms(pages["main"])
    global_rank = get_similarweb_rank(get_domain_from_url(pages["main"]), api_key)
    
    return {
        "Base URL": base_url,
        "Emails": list(combined_emails),
        "Telephones": list(combined_telephones),
        "Company Name": company_name,
        "Sector": sector,
        "Global Rank": global_rank,
        "Used Tool": cms,
        "Pixels": combined_pixels,
        "Ad Activity": combined_ad_activity
    }
