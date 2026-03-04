# Flights (Global Flight Tracking)

Flight tracking, delays, and cancellations.

## When to Use This File

- Query mentions: flight, airport, delay, cancellation, airline
- Query is about: Flight status, arrivals, departures
- No specific country mentioned

## Live Flight Tracking

### Flightradar24
- **URL:** https://www.flightradar24.com
- **Coverage:** Global
- **Best for:** Live aircraft positions, flight paths
- **Example:** "Track LH123" -> search on site

### FlightAware
- **URL:** https://www.flightaware.com
- **Best for:** Flight tracking with predictions
- **Example:** "UA456 status"

### ADS-B Exchange
- **URL:** https://globe.adsbexchange.com
- **Best for:** Free flight tracking, no rate limits

## Cancellations and Delays

### FlightAware Cancellations
- **URL:** https://www.flightaware.com/live/cancelled/
- **Best for:** See all cancelled flights by airline/airport
- **Example:** "Lufthansa cancellations today"

### FlightStats Airport Delays
- **URL:** https://www.flightstats.com/v2/airport-delays
- **Best for:** Airport-wide delay overview
- **Example:** "Which European airports have delays?"

### FlightStats Flight Tracker
- **URL:** https://www.flightstats.com/v2/flight-tracker/search
- **Best for:** Search by flight number

## Free Flight APIs

### ADS-B Exchange API
- **URL:** https://www.adsbexchange.com/data/
- **Cost:** Free, no rate limits
- **Data:** Real-time aircraft positions

### OpenSky Network API
- **URL:** https://opensky-network.org/api/states/all
- **Cost:** Free (100 req/day anonymous, 4000/day registered)
- **Data:** Live ADS-B aircraft data

### Aviationstack
- **URL:** https://aviationstack.com
- **Cost:** 100 requests/month free
- **Data:** Flight status, airports, airlines
