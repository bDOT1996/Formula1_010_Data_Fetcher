# Filtry dla tabel OpenF1 API

Ten dokument zawiera listę możliwych filtrów dla każdej tabeli (endpointu) dostępnej w OpenF1 API, wraz z przykładami żądań HTTP GET. Filtry są oparte na atrybutach każdej tabeli, które można wykorzystać w parametrach URL, zgodnie z dokumentacją [OpenF1 API](https://openf1.org). Atrybuty tablicowe nie są obsługiwane w filtrowaniu.

## Tabela `meetings`
**Opis**: Przechowuje informacje o wydarzeniach Grand Prix (np. Monaco GP 2023).

**Możliwe filtry**:
- `meeting_key` (integer): Unikalny identyfikator wydarzenia.
- `circuit_key` (integer): Identyfikator toru.
- `circuit_short_name` (varchar): Krótka nazwa toru (np. "Monaco").
- `country_code` (varchar): Kod kraju (np. "MCO").
- `date_start` (timestamp): Data rozpoczęcia wydarzenia (np. "2023-05-28").
- `gmt_offset` (varchar): Przesunięcie czasowe GMT (np. "+02:00").
- `meeting_name` (varchar): Nazwa wydarzenia (np. "Monaco Grand Prix").
- `year` (integer): Rok wydarzenia (np. 2023).

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/meetings?year=2023&circuit_short_name=Monaco
```

## Tabela `sessions`
**Opis**: Przechowuje informacje o sesjach (treningi, kwalifikacje, wyścigi) w ramach wydarzenia.

**Możliwe filtry**:
- `session_key` (integer): Unikalny identyfikator sesji.
- `meeting_key` (integer): Identyfikator wydarzenia.
- `circuit_key` (integer): Identyfikator toru.
- `circuit_short_name` (varchar): Krótka nazwa toru.
- `country_code` (varchar): Kod kraju.
- `date_start` (timestamp): Data rozpoczęcia sesji.
- `date_end` (timestamp): Data zakończenia sesji.
- `session_name` (varchar): Nazwa sesji (np. "Race").
- `session_type` (varchar): Typ sesji (np. "Practice", "Qualifying", "Race").

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/sessions?meeting_key=12345&session_type=Race
```

## Tabela `drivers_in_session`
**Opis**: Przechowuje szczegóły kierowców w danej sesji.

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `driver_number` (integer): Numer kierowcy (np. 33 dla Maxa Verstappena).
- `broadcast_name` (varchar): Nazwa wyświetlana w transmisji (np. "M VERSTAPPEN").
- `country_code` (varchar): Kod kraju kierowcy (np. "NLD").
- `first_name` (varchar): Imię kierowcy.
- `full_name` (varchar): Pełne imię i nazwisko kierowcy.
- `headshot_url` (varchar): URL zdjęcia kier Cecilia kierowcy.
- `team_name` (varchar): Nazwa zespołu (np. "Red Bull Racing").

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/drivers?session_key=67890&team_name=Red+Bull+Racing
```

## Tabela `laps`
**Opis**: Przechowuje dane o okrążeniach dla każdego kierowcy w sesji.

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `driver_number` (integer): Numer kierowcy.
- `lap_number` (integer): Numer okrążenia.
- `date_start` (timestamp): Data rozpoczęcia okrążenia.
- `duration_sector_1` (float): Czas sektora 1 (w sekundach).
- `duration_sector_2` (float): Czas sektora 2.
- `duration_sector_3` (float): Czas sektora 3.
- `i1_speed` (integer): Prędkość na pierwszym punkcie pomiarowym (km/h).
- `i2_speed` (integer): Prędkość na drugim punkcie pomiarowym.
- `lap_duration` (float): Czas całego okrążenia.
- `st_speed` (integer): Prędkość na prostej startowej.

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/laps?session_key=67890&driver_number=33&lap_duration<=80
```

## Tabela `stints`
**Opis**: Przechowuje informacje o stintach oponowych dla każdego kierowcy.

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `driver_number` (integer): Numer kierowcy.
- `stint_number` (integer): Numer stintu.
- `compound` (varchar): Typ mieszanki opon (np. "Soft", "Medium", "Hard").
- `lap_start` (integer): Numer okrążenia rozpoczęcia stintu.
- `lap_end` (integer): Numer okrążenia zakończenia stintu.
- `tyre_age` (integer): Wiek opon w liczbie okrążeń.

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/stints?session_key=67890&driver_number=33&compound=Soft
```

## Tabela `pit_stops`
**Opis**: Przechowuje szczegóły pit-stopów.

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `driver_number` (integer): Numer kierowcy.
- `lap_number` (integer): Numer okrążenia pit-stopu.
- `date` (timestamp): Data i czas pit-stopu.
- `pit_duration` (float): Czas trwania pit-stopu (w sekundach).

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/pit?session_key=67890&driver_number=33&pit_duration<=25
```

## Tabela `car_data`
**Opis**: Przechowuje dane telemetryczne samochodów (~3,7 Hz).

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `driver_number` (integer): Numer kierowcy.
- `date` (timestamp): Data i czas próbki telemetrycznej.
- `brake` (integer): Poziom hamowania (0-100).
- `drs` (integer): Status DRS (np. 0 = wyłączony, 1 = włączony).
- `n_gear` (integer): Bieg (np. 1-8).
- `rpm` (integer): Obroty silnika (obr./min).
- `speed` (integer): Prędkość (km/h).
- `throttle` (integer): Poziom gazu (0-100).

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/car_data?session_key=67890&driver_number=33&speed>=315
```

## Tabela `location`
**Opis**: Przechowuje współrzędne pozycji samochodów (~3,7 Hz).

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `driver_number` (integer): Numer kierowcy.
- `date` (timestamp): Data i czas próbki pozycji.
- `x` (float): Współrzędna X na torze.
- `y` (float): Współrzędna Y na torze.
- `z` (float): Współrzędna Z na torze.

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/location?session_key=67890&driver_number=33&x>=1000
```

## Tabela `position`
**Opis**: Przechowuje bieżące pozycje kierowców w sesji.

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `driver_number` (integer): Numer kierowcy.
- `date` (timestamp): Data i czas próbki pozycji.
- `position` (integer): Pozycja kierowcy (np. 1, 2, 3).

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/position?session_key=67890&driver_number=33&position=1
```

## Tabela `intervals`
**Opis**: Przechowuje różnice czasowe do lidera (tylko dla sesji wyścigowych).

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `driver_number` (integer): Numer kierowcy.
- `date` (timestamp): Data i czas próbki interwału.
- `gap_to_leader` (float): Różnica czasowa do lidera (w sekundach).
- `interval` (float): Różnica czasowa do poprzedzającego kierowcy.

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/intervals?session_key=67890&driver_number=33&gap_to_leader<=2.5
```

## Tabela `team_radio`
**Opis**: Przechowuje komunikaty radiowe zespołu.

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `driver_number` (integer): Numer kierowcy.
- `date` (timestamp): Data i czas komunikatu radiowego.
- `recording_url` (varchar): URL nagrania komunikatu.

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/team_radio?session_key=67890&driver_number=33
```

## Tabela `weather`
**Opis**: Przechowuje dane pogodowe, aktualizowane co minutę.

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `date` (timestamp): Data i czas próbki pogodowej.
- `air_temperature` (float): Temperatura powietrza (°C).
- `humidity` (float): Wilgotność (%).
- `pressure` (float): Ciśnienie atmosferyczne (mbar).
- `rainfall` (integer): Opady (0 = brak, 1 = opady).
- `track_temperature` (float): Temperatura toru (°C).
- `wind_direction` (integer): Kierunek wiatru (stopnie).
- `wind_speed` (float): Prędkość wiatru (km/h).

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/weather?session_key=67890&rainfall=1
```

## Tabela `race_control`
**Opis**: Przechowuje komunikaty kontroli wyścigu (np. flagi, incydenty).

**Możliwe filtry**:
- `session_key` (integer): Identyfikator sesji.
- `date` (timestamp): Data i czas komunikatu.
- `category` (varchar): Kategoria komunikatu (np. "Flag", "Incident").
- `flag` (varchar): Rodzaj flagi (np. "Yellow", "Red").
- `lap_number` (integer): Numer okrążenia, do którego odnosi się komunikat.
- `message` (text): Treść komunikatu.
- `scope` (varchar): Zakres komunikatu (np. "Sector", "Track").

**Przykład żądania**:
```bash
GET https://api.openf1.org/v1/race_control?session_key=67890&flag=Yellow
```

## Uwagi
- **Format filtrowania**: Filtry są dodawane do URL jako parametry, np. `?session_key=67890&driver_number=33`. Można łączyć wiele filtrów za pomocą `&`.
- **Obsługa dat**: Atrybuty typu `timestamp` obsługują różne formaty, np. "2023-05-28" lub "2023-05-28T14:00:00".
- **Ograniczenia**: Atrybuty tablicowe nie mogą być używane jako filtry. API obsługuje tylko filtry dla atrybutów skalarnych.
- **Efektywność**: Dla dużych datasetów (np. `car_data`, `location`) używaj filtrów, aby ograniczyć dane, np. `speed>=315` lub `date>=2023-05-28T14:00:00`.
- **Format CSV**: Dodaj `csv=true` do URL, aby pobrać dane w formacie CSV, np. `https://api.openf1.org/v1/laps?session_key=67890&csv=true`.

## Źródła
- [Dokumentacja OpenF1 API](https://openf1.org)
- [OpenF1 GitHub](https://github.com/theOehrly/FastF1)

**Data aktualizacji**: 26 maja 2025, 00:12 CEST