# Wind_Data_Live File

This file pulls live weather data from the US Air Force Academy Mesonet (HWAS) and saves key values to a CSV for drone flight testing. The goal is to capture local wind conditions at or near the test site so flight data can be paired with real environmental conditions during each test window.

## What is HWAS?
- HWAS = High Wind Alert System (US Air Force Academy Mesonet)
- A mesonet is a network of weather stations across one area
- It gives more local detail than relying on one single weather source

## Why we use it
- Supports flight test site awareness
- Helps document wind conditions during drone operations
- Lets us compare flight performance against actual weather
- Gives context for gusts, crosswinds, and changing local conditions

## Key data collected
- Timestamp
- Station name
- Wind direction (deg)
- Wind speed (kt)
- Wind gust (kt)
- Barometric pressure (in Hg)

## Other fields shown on HWAS (we're not using)
- Relative humidity (%)
- Precipitation (in)
- Wind chill (deg F)
- Heat index / heat stress

## Units
- Direction = degrees
- Speed = knots
- Gust = knots
- Temperature = degrees Fahrenheit
- Pressure = inches of mercury
- Precipitation = inches

## Update rate
- HWAS page auto-refreshes every 30 seconds
- Station rows show a "Last Report" time
- Page header states update time in UTC


## Source
- https://hwas.usafa.edu/
