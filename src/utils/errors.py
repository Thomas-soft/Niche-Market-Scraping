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
    console.print("[red]Error:[/red] The number of sites must be an integer.")
    sys.exit(1)


def must_be_float_error():
    """
    Display an error message when the latitude and longitude are not floats.
    """
    console.print("[red]Error:[/red] Latitude and longitude must be floats.")
    sys.exit(1)


def element_not_found_error(reason):
    """
    Display an error message when an element is not found.
    """
    console.print(f"[red]Error:[/red] Element not found.\nReason: {reason}")
    sys.exit(1)


def save_error(reason):
    """
    Display an error message when the results cannot be saved.
    """
    console.print("[red]Error:[/red] Unable to save the results.\nReason: {reason}")
    sys.exit(1)
