from urllib.parse import urlparse


def get_domain_from_url(url):
    """
    Extrait le domaine (ex: "www.example.com") d'une URL complète.
    """
    parsed = urlparse(url)
    return parsed.netloc


def get_pages(base_url):
    """
    Construit les URL pour la page principale, la page de contact et la page 'À propos'.
    On suppose que base_url est du type "https://www.example.com" sans slash terminal.
    """
    if base_url.endswith('/'):
        base_url = base_url[:-1]
    pages = {
        "main": base_url,
        "contact": base_url + "/contact",
        "about": base_url + "/about"
    }
    return pages
