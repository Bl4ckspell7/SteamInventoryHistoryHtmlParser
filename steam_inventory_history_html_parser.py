from bs4 import BeautifulSoup
import csv
import tkinter as tk
from tkinter import filedialog
from unidecode import unidecode

# User selects the HTML file
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename(filetypes=[("HTML files", "*.html")])

# HTML-Datei parsen
with open(file_path, "r", encoding="utf-8") as file:
    soup = BeautifulSoup(file, "html.parser")

# Open CSV file for writing
csv_file_path = "output.csv"
csv_file = open(csv_file_path, "w", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(
    ["Date", "Timestamp", "Event Description", "Items Plus/Minus", "Item Name"]
)

# Extract entries and write to CSV
trade_history_rows = soup.find_all("div", class_="tradehistoryrow")
for row in trade_history_rows:
    date = row.find("div", class_="tradehistory_date").get_text(strip=True)
    timestamp = row.find("div", class_="tradehistory_timestamp").get_text(strip=True)
    event_description = row.find(
        "div", class_="tradehistory_event_description"
    ).get_text(strip=True)

    items_plusminus_elem = row.find("div", class_="tradehistory_items_plusminus")
    items_plusminus = (
        items_plusminus_elem.get_text(strip=True) if items_plusminus_elem else ""
    )
    item_name = row.find("span", class_="history_item_name").get_text(strip=True)

    # knifes have a star in their name which gives an error when writing to .csv
    item_name = unidecode(item_name)

    # some "traded with 'player names'" have not encodable characters as well
    event_description = unidecode(event_description)

    date = date.replace(",", "")

    csv_writer.writerow(
        [date, timestamp, event_description, items_plusminus, item_name]
    )

# Close CSV file
csv_file.close()

print(f'The extracted data was successfully stored in "{csv_file_path}".')
