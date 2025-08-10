# f1-data-fetcher

Kontenerowy fetcher danych F1 z API Ergast, zapisujący dane do współdzielonego volumen-u (np. /data/bronze).

## Jak używać:

```
docker build -t f1-fetcher .
docker run --rm -v f1_shared_volume:/data f1-fetcher
```

Albo z docker-compose:

```
docker compose -f docker-compose.override.yml up --build
```

## Dane:
Pliki .parquet zapisują się w: /data/bronze/raw/


# OpenF1 Data Fetcher

## Overview
This project is designed to fetch, store, and analyze Formula 1 data from the [OpenF1 API](https://openf1.org). The OpenF1 API provides real-time and historical data about Formula 1 races, including lap times, telemetry, driver information, weather conditions, and more. The project aims to retrieve these datasets and store them in a structured database based on the Entity-Relationship (ER) model described below. The data can be used for race analysis, visualization, or predictive modeling.

## Project Scope
The OpenF1 Data Fetcher retrieves data from the OpenF1 API, which is a free, open-source API offering comprehensive Formula 1 data starting from 2018. The project supports:
- Fetching data for Grand Prix events, sessions, drivers, laps, telemetry, and other related information.
- Storing data in a relational database with the schema outlined in the ER diagram.
- Providing a foundation for further analysis, such as lap time comparisons, telemetry visualization, or stint strategy evaluation.

## Entity-Relationship Diagram
The database schema is designed to reflect the structure of the OpenF1 API datasets. Below is the ER diagram representing the relationships between the entities:

![ER Diagram](er_diagram.png)

### Schema Description
The schema consists of the following tables and relationships:

- **meetings**: Stores information about Grand Prix events (e.g., Monaco GP 2023).
- **sessions**: Stores race sessions (e.g., practice, qualifying, race) linked to a meeting.
- **drivers_in_session**: Stores driver details for each session.
- **laps**: Stores lap times and sector data for each driver in a session.
- **stints**: Stores tire stint information for each driver.
- **pit_stops**: Stores pit stop details.
- **car_data**: Stores telemetry data (e.g., speed, RPM) sampled at ~3.7 Hz.
- **location**: Stores car position coordinates.
- **position**: Stores driver positions during a session.
- **intervals**: Stores time gaps to the leader (race sessions only).
- **team_radio**: Stores team radio communications.
- **weather**: Stores weather conditions, updated every minute.
- **race_control**: Stores race control messages (e.g., flags, incidents).



| Encja                | Klucz główny                          | Atrybuty                                                                 | Opis                                          |
|----------------------|---------------------------------------|--------------------------------------------------------------------------|-----------------------------------------------|
| Meeting              | meeting_key                           | circuit_key, circuit_short_name, country_code, date_start, gmt_offset, meeting_name, year | Wydarzenie Grand Prix (np. Bahrain GP 2023). |
| Session              | session_key                           | circuit_key, circuit_short_name, country_code, date_end, date_start, session_name, session_type | Sesja w ramach wydarzenia (trening, wyścig). |
| DriverInSession      | (session_key, driver_number)          | broadcast_name, country_code, first_name, full_name, headshot_url, team_name | Kierowca w konkretnej sesji.                 |
| Lap                  | (session_key, driver_number, lap_number) | date_start, duration_sector_1, duration_sector_2, duration_sector_3, i1_speed, i2_speed, lap_duration, st_speed | Okrążenie wykonane przez kierowcę.           |
| Stint                | (session_key, driver_number, stint_number) | compound, lap_end, lap_start, tyre_age                                   | Stint oponowy kierowcy.                     |
| PitStop              | (session_key, driver_number, lap_number) | date, pit_duration                                                     | Postój w pit-stopie.                        |
| CarData              | (session_key, driver_number, date)    | brake, drs, n_gear, rpm, speed, throttle                                 | Dane telemetryczne samochodu (~3.7 Hz).      |
| Location             | (session_key, driver_number, date)    | x, y, z                                                                 | Położenie samochodu na torze.               |
| Position             | (session_key, driver_number, date)    | position                                                                | Bieżąca pozycja kierowcy.                   |
| Interval             | (session_key, driver_number, date)    | gap_to_leader, interval                                                 | Interwały czasowe (tylko wyścigi).          |
| TeamRadio            | (session_key, driver_number, date)    | recording_url                                                           | Komunikaty radiowe dla kierowcy.            |
| Weather              | (session_key, date)                   | air_temperature, humidity, pressure, rainfall, track_temperature, wind_direction, wind_speed | Dane pogodowe aktualizowane co minutę.      |
| RaceControlMessage   | (session_key, date)                   | category, flag, lap_number, message, scope                               | Komunikaty kontroli wyścigu.                |


**Relationships**:
- One `meeting` has many `sessions` (via `meeting_key`).
- One `session` has many `drivers_in_session` (via `session_key`).
- One `driver_in_session` has many `laps`, `stints`, `pit_stops`, `car_data`, `location`, `position`, `intervals`, and `team_radio` (via `session_key` and `driver_number`).
- One `session` has many `weather` and `race_control` records (via `session_key`).

## Data Fetching Strategy
To efficiently retrieve data while respecting the API's structure and limits, follow this order:
1. **Meetings**: Fetch all Grand Prix events for a season (e.g., `GET https://api.openf1.org/v1/meetings?year=2023`).
2. **Sessions**: For each `meeting_key`, fetch sessions (e.g., `GET https://api.openf1.org/v1/sessions?meeting_key=12345`).
3. **Drivers in Session**: For each `session_key`, fetch driver details (e.g., `GET https://api.openf1.org/v1/drivers?session_key=67890`).
4. **Driver-Specific Data**: For each `session_key` and `driver_number`, fetch:
   - Lap times (`laps`)
   - Tire stints (`stints`)
   - Pit stops (`pit_stops`)
   - Telemetry (`car_data`, use filters like `speed>=315` for efficiency)
   - Position (`position`)
   - Intervals (`intervals`, race only)
   - Team radio (`team_radio`)
5. **Session-Specific Data**: For each `session_key`, fetch:
   - Weather (`weather`)
   - Race control messages (`race_control`)

**Note**: The API has a 1-minute query timeout, so split large requests (e.g., telemetry data) using filters like date ranges or specific attributes.

## Requirements
- **Python**: Version >= 3.10
- **Libraries**:
  - `requests`: For making HTTP requests to the OpenF1 API.
  - `pandas`: For handling CSV data and data analysis.
  - Install with: `pip install requests pandas`

## Example Usage
Below is a basic Python script to fetch and print lap times for a specific driver in a session:
```python
import requests

url = "https://api.openf1.org/v1/laps?session_key=67890&driver_number=33"
response = requests.get(url)
if response.status_code == 200:
    lap_data = response.json()
    print(lap_data)
else:
    print(f"Error: {response.status_code}")
```

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/openf1-data-fetcher.git
   cd openf1-data-fetcher
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure the database (e.g., SQLite, PostgreSQL) using the schema provided in the ER diagram.
4. Run the data fetcher script to populate the database.

## Future Enhancements
- Implement data caching to reduce API calls.
- Add visualization tools for lap times, telemetry, and stint strategies.
- Support for real-time data streaming during live races.
- Integration with machine learning models for race predictions.

## Contributing
Contributions are welcome! Please submit issues or pull requests to the [GitHub repository](https://github.com/your-repo/openf1-data-fetcher). For questions, contact the maintainers or use the [OpenF1 contact form](https://openf1.org/contact).

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## References
- [OpenF1 API Documentation](https://openf1.org)
- [OpenF1 GitHub](https://github.com/theOehrly/FastF1)


