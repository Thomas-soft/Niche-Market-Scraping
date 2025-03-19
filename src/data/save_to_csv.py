import csv
import os
from config.console import console
from utils.errors import save_error


def save_results(results, filename):
    """
    Saves the results into a CSV file.

    Args:
        results (list): A list of results (e.g., URLs or site names) to be saved.
        filename (str): The name of the CSV file (default is "data.csv").
    """
    # Create the directory if it does not exist
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            # Write header row (optional)
            writer.writerow(["Websites"])
            for result in results:
                writer.writerow([result.split(" ")[0]])
        console.print(f"[green]Results successfully saved in {filename}.[/green]")
    except Exception as e:
        save_error(f"An error occurred while saving the results to {filename}: {e}")


def save_all_infos(results, filename):
    """
    Saves the scraped site information into a CSV file.
    
    Each result is a dictionary with the following keys:
      - base_url: str
      - emails: list of strings
      - telephones: list of strings
      - nom_entreprise: str (Company Name)
      - secteur: str (Sector)
      - rang_global: str or int (Global Rank)
      - outil_utilisé: str (Used Tool, e.g., CMS)
      - pixels: dict of booleans (e.g., {"facebook_pixel": True, "google_analytics": False, ...})
      - activite_publicitaire: dict of booleans (e.g., {"google_ads": True, "facebook_ads": False, ...})
    
    For fields with multiple values, the items are joined by " ; ".
    For the dictionary fields, only the keys with a True value are output.
    
    Args:
        results (list): List of dictionaries containing the scraped site data.
        filename (str): The CSV file to write the results to (default is "data.csv").
    """
    # Define CSV headers in English
    headers = [
        "Base URL",
        "Emails",
        "Telephones",
        "Company Name",
        "Sector",
        "Global Rank",
        "Used Tool",
        "Pixels",
        "Ad Activity"
    ]
    
    # Create directory if needed
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)
    
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers)
            for result in results:
                base_url = result.get("Base URL", "")
                # For list fields, join with " ; "
                emails = " ; ".join(result.get("Emails", [])) if isinstance(result.get("Emails", []), list) else result.get("Emails", "")
                telephones = " ; ".join(result.get("Telephones", [])) if isinstance(result.get("Telephones", []), list) else result.get("Telephones", "")
                company_name = result.get("Company Name", "")
                sector = result.get("Sector", "")
                global_rank = result.get("Global Rank", "")
                used_tool = result.get("Used Tool", []) if isinstance(result.get("Used Tool", []), list) else result.get("Used Tool", "")
                
                # For dictionary fields, output only keys with a True value
                pixels_dict = result.get("Pixels", {})
                if isinstance(pixels_dict, dict):
                    pixels = " ; ".join([key for key, value in pixels_dict.items() if value])
                else:
                    pixels = pixels_dict

                ad_activity_dict = result.get("Ad Activity", {})
                if isinstance(ad_activity_dict, dict):
                    ad_activity = " ; ".join([key for key, value in ad_activity_dict.items() if value])
                else:
                    ad_activity = ad_activity_dict

                writer.writerow([
                    base_url,
                    emails,
                    telephones,
                    company_name,
                    sector,
                    global_rank,
                    used_tool,
                    pixels,
                    ad_activity
                ])
        console.print(f"[green]Results successfully saved to {filename}.[/green]")
    except Exception as e:
        console.print(f"[red]Error saving CSV file: {e}[/red]")
