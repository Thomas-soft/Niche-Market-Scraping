from config.console import console
from rich.panel import Panel


def bot_configuration_info(search_query, number_of_sites):
    """
    Display a summary of the bot configuration in a panel.
    """
    panel_text = (
        f"[bold green]Search request :[/bold green] {search_query}\n"
        f"[bold blue]Number of sites :[/bold blue] {number_of_sites}"
    )
    console.print(Panel(panel_text, title="[bold magenta]Bot Configuration[/bold magenta]", expand=False))


def welcome_message(search_query, number_of_sites):
    """
    Display a welcome message in a panel.
    """
    welcome_message = (
        "[bold magenta]Scraping[/bold magenta]\n\n"
        "This bot will scrape the first [bold]n[/bold] websites from a Google search query.\n"
        f"The search query is: [bold blue]{search_query}[/bold blue]\n"
        f"The number of websites to scrape is: [bold blue]{number_of_sites}[/bold blue]\n\n"
        "The bot will start scraping the websites...\n"
        "Please wait until the process is finished.\n"
    )
    console.print(Panel(welcome_message, title="[bold blue]Niche Market Scraping[/bold blue]", expand=False))


def finished_info():
    """
    Display a process finished message in a panel.
    """
    console.print(Panel("[bold green]Scraping finished![/bold green]", title="[bold blue]End of process[/bold blue]", expand=False))