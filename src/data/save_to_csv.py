# File: utils/save_data.py
import csv
import os
from config.console import console
from utils.errors import save_error


def save_results(results, filename="data.csv"):
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
