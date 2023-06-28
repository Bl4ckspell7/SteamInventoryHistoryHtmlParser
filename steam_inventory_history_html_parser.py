from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import filedialog
from unidecode import unidecode
from tqdm import tqdm  # Import tqdm for the progress bar

try:
    # User selects the HTML file
    root = tk.Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html;*.htm")])

    # Parse HTML file
    with open(file_path, "r", encoding="utf-8") as file:
        print("Reading HTML...")
        soup = BeautifulSoup(file, "html.parser")

    # Open CSV file for writing
    default_csv_file_name = "output.csv"
    csv_file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        initialfile=default_csv_file_name,
        title="Save CSV file",
    )
    csv_file = open(csv_file_path, "w", newline="")
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ["Date", "Timestamp", "Event Description", "Items Plus/Minus", "Item Name"]
    )

    print("Parsing data...")

    # Extract entries and write to CSV
    trade_history_rows = soup.find_all("div", class_="tradehistoryrow")

    # Create a progress bar using tqdm
    progress_bar = tqdm(
        total=len(trade_history_rows), bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}"
    )

    for row in trade_history_rows:
        # TIME ENTRY
        timestamp_element = row.find("div", class_="tradehistory_timestamp")
        timestamp = timestamp_element.get_text(strip=True)
        # remove timestamp from date entry, otherwise date contains the time
        timestamp_element.decompose()

        # DATE ENTRY
        date = row.find("div", class_="tradehistory_date").get_text(strip=True)
        date = date.replace(",", ".")

        # DESCRIPTION ENTRY
        event_description = row.find(
            "div", class_="tradehistory_event_description"
        ).get_text(strip=True)
        event_description = unidecode(event_description)

        # ITEM AQUIRED OR GIVEN ENTRY
        items_plusminus_elem = row.find("div", class_="tradehistory_items_plusminus")
        items_plusminus = (
            items_plusminus_elem.get_text(strip=True) if items_plusminus_elem else ""
        )

        # ITEM NAME ENTRY
        item_name = row.find("span", class_="history_item_name").get_text(strip=True)
        # knifes have a star in their name which causes an error when writing to .csv
        item_name = unidecode(item_name)
        # some "traded with 'player names'" strings have not encodable characters as well

        csv_writer.writerow(
            [date, timestamp, event_description, items_plusminus, item_name]
        )

        # Update the progress bar
        progress_bar.update(1)

    # Close the progress bar
    progress_bar.close()

    # Close CSV file
    csv_file.close()

    print(f'The extracted data was successfully stored in "{csv_file_path}".')

except Exception as e:
    print(f"An error has occurred: {str(e)}")

input("Press Enter to close...")
