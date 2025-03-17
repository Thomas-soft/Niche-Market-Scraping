import sys
from config.console import console
from rich.panel import Panel


def usage_error():
    """
    Display an error message when the script is not used correctly
    """
    console.print(
        Panel(
            "[red]Usage :[/red] python3 <script> [blue]<request search google> <number of websites to scrape> <latitude (optional)> <longitude (optional)>",
            title="[bold red]Error[/bold red]",
            expand=False,
        )
    )
    sys.exit(1)


def must_be_integer_error():
    """
    Display an error message when the number of sites is not an integer.
    """
    console.print("[red]Erreur:[/red] The number of sites must be an integer.")
    sys.exit(1)


def must_be_float_error():
    """
    Display an error message when the latitude and longitude are not floats.
    """
    console.print("[red]Erreur:[/red] Latitude and longitude must be floats.")
    sys.exit(1)