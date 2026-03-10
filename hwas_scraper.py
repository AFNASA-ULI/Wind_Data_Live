import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime
import os

url = "https://hwas.usafa.edu/"
csv_filename = r"C:\Users\C27Jillian.Essig\OneDrive - afacademy.af.edu\Desktop\hwas_wind_data.csv"

print(f"CSV will be saved to: {csv_filename}")
print(f"Current working directory: {os.getcwd()}")

start_time = time.time()
run_duration = 5 * 60    # 5 minutes
interval = 30            # scrape every 30 seconds

# Create CSV file and write header first
with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Timestamp", "Direction (deg)", "Speed (kt)", "Gust (kt)"])

print("CSV header created successfully.")

# Run scraper loop
while time.time() - start_time < run_duration:
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        cadet_row = soup.find("tr", id="4")

        if cadet_row is None:
            print("Could not find row with id='4'")
        else:
            columns = cadet_row.find_all("td")

            direction_raw = columns[1].text.strip()
            speed_raw = columns[2].text.strip()
            gust_raw = columns[3].text.strip()

            direction = direction_raw.replace("Direction:", "").strip()
            speed = speed_raw.replace("Speed:", "").strip()
            gust = gust_raw.replace("Gust:", "").strip()

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Append one row immediately to CSV
            with open(csv_filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([timestamp, direction, speed, gust])

            print("\n--- Cadet Area Wind ---")
            print(f"Time:      {timestamp}")
            print(f"Direction: {direction}°")
            print(f"Speed:     {speed} kt")
            print(f"Gust:      {gust} kt\n")
            print(f"Saved row to: {csv_filename}")

    except Exception as e:
        print(f"Error during scrape: {e}")

    time.sleep(interval)

print(f"Data collection complete. Saved to {csv_filename}")