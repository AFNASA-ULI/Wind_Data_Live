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

start_time = time.time()
run_duration = 5 * 60
interval = 30

def extract_number(text):
    match = re.search(r"-?\d+\.?\d*", text)
    return match.group() if match else ""

with open(csv_filename, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow([
        "Timestamp",
        "Direction (deg)",
        "Speed (kt)",
        "Gust (kt)",
        "Temperature (F)",
        "Humidity (%)"
    ])

print("CSV header created successfully.")

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

            with open(csv_filename, mode="a", newline="") as file:
                writer = csv.writer(file)
                writer.writerow([
                    timestamp,
                    direction,
                    speed,
                    gust,
                    temperature,
                    humidity
                ])

            print("\n--- Cadet Area Weather ---")
            print(f"Time:        {timestamp}")
            print(f"Direction:   {direction}°")
            print(f"Speed:       {speed} kt")
            print(f"Gust:        {gust} kt")
            print(f"Temperature: {temperature} F")
            print(f"Humidity:    {humidity} %\n")

    except Exception as e:
        print(f"Error during scrape: {e}")

    time.sleep(interval)

print(f"Data collection complete. Saved to {csv_filename}")