import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
import os
import re

url = "https://hwas.usafa.edu/"

timestamp_for_file = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = rf"C:\Users\C27Jillian.Essig\OneDrive - afacademy.af.edu\Desktop\hwas_wx_data_{timestamp_for_file}.csv"

print(f"CSV will be saved to: {csv_filename}")
print(f"Current working directory: {os.getcwd()}")

interval = 30
start_time = time.time()

def extract_number(text):
    match = re.search(r"-?\d+\.?\d*", text)
    return match.group() if match else ""

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Timestamp",
        "Elapsed Seconds",
        "Direction (deg)",
        "Speed (kt)",
        "Gust (kt)",
        "Temperature (F)",
        "Humidity (%)"
    ])

print("CSV header created successfully.")
print("Scraper is running. Press Ctrl+C to stop.\n")

try:
    while True:
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")

            cadet_row = soup.find("tr", id="4")

            if cadet_row is None:
                print("Could not find row with id='4'")
            else:
                columns = cadet_row.find_all("td")

                direction_raw = columns[1].get_text(" ", strip=True)
                speed_raw = columns[2].get_text(" ", strip=True)
                gust_raw = columns[3].get_text(" ", strip=True)
                temperature_raw = columns[4].get_text(" ", strip=True)
                humidity_raw = columns[5].get_text(" ", strip=True)

                direction = extract_number(direction_raw)
                speed = extract_number(speed_raw)
                gust = extract_number(gust_raw)
                temperature = extract_number(temperature_raw)
                humidity = extract_number(humidity_raw)

                timestamp = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                elapsed_seconds = int(time.time() - start_time)

                try:
                    with open(csv_filename, mode="a", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow([
                            timestamp,
                            elapsed_seconds,
                            direction,
                            speed,
                            gust,
                            temperature,
                            humidity
                        ])

                    print("\n--- Cadet Area Weather ---")
                    print(f"Time:            {timestamp}")
                    print(f"Elapsed Seconds: {elapsed_seconds}")
                    print(f"Direction:       {direction}°")
                    print(f"Speed:           {speed} kt")
                    print(f"Gust:            {gust} kt")
                    print(f"Temperature:     {temperature} F")
                    print(f"Humidity:        {humidity} %")

                except PermissionError:
                    print("\nCould not write to CSV because the file is open in Excel or locked.")
                    print("Close the CSV and the script will try again on the next cycle.")

        except Exception as e:
            print(f"Error during scrape: {e}")

        time.sleep(interval)

except KeyboardInterrupt:
    print(f"\n\nScraper stopped by user.")
    print(f"Data saved to: {csv_filename}")