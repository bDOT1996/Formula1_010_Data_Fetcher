from typing import Dict, Any, Optional
from datetime import datetime

import requests
import pandas as pd
import time
import logging

from .class_APIRequestBuilder import *

# Initialize logger
logger = logging.getLogger(__name__)

class APIClient:
    def __init__(self, api_url):
        self.api_url = api_url
        self.builder = {
            # Tier 1
            "meetings": MeetingsRequestBuilder(),
            # Tier 2
            "sessions": SessionsRequestBuilder(),
            # Tier 3
            "drivers": DriversRequestBuilder(),
            "race_control": RaceControlRequestBuilder(),
            "session_result": SessionResultRequestBuilder(),
            "starting_grid": StartingGridRequestBuilder(),
            "stints": StintsRequestBuilder(),
            "team_radio": TeamRadioRequestBuilder(),
            "weather": WeatherRequestBuilder(),
            # Tier 4
            "laps": LapsRequestBuilder(),
            "overtakes": OvertakesRequestBuilder(),
            "pit": PitRequestBuilder(),
            "position": PositionRequestBuilder(),
            # Tier 5.1
            "intervals": IntervalsRequestBuilder(),
            # Tier 5.2
            "car_data": CarDataRequestBuilder(),
            "location": LocationRequestBuilder()
        }

    def fetch_data(self, endpoint: str, params: Dict[str, Any]) -> pd.DataFrame:
        """
        Builds payload, calls API (mock), returns pandas.DataFrame with correct schema.
        """
        if endpoint not in self.builder:
            raise ValueError(f"Unknown endpoint: {endpoint}")

        builder = self.builder[endpoint]
        payload = builder.build_payload(params)

        url = f"{self.api_url}/{endpoint}"

        response_json = self._mock_api_call(api_data=payload, api_url=url)

        schema = builder.get_schema()

        # Log for debugging
        logger.debug(f"API response from {endpoint}: {response_json}")

        if not response_json:  # Handle empty response
            logger.warning(f"Empty API response from {endpoint}, returning empty DataFrame with schema.")
            df = pd.DataFrame(columns=schema.keys()).astype(schema)
        else:
            df = pd.DataFrame(response_json)
            logger.debug(f"DataFrame columns: {df.columns.tolist()}")
            df = df.astype(schema)

        return df
    
    def _mock_api_call(
        self,
        api_data: Dict[str, Any],
        api_url: str,
        max_attempts: int = 5,
        backoff: int = 5,
        timeout: tuple = (5, 15)
    ) -> Optional[Dict[str, Any]]:
        
        for attempt in range(1, max_attempts + 1):
            logger.info(f"Attempt {attempt} with parameters: {api_data}")
            
            try:
                response = requests.get(
                    url=api_url,
                    params=api_data,
                    timeout=timeout
                )
        
            except requests.exceptions.RequestException as exc:
                logger.warning(f"Network error on attempt {attempt}: {exc}")
                # Continue to retry
            
            else:
                status = response.status_code
                reason = response.reason
                
                if status == 200:
                    try:
                        response_json = response.json()
                    except ValueError as exc:
                        logger.error(f"Invalid JSON on attempt {attempt}: {exc}")
                        # Continue to retry
                    else:
                        if not response_json:  # Checks None, [], {} - all falsy
                            logger.warning(f"Empty response on attempt {attempt}, parameters={api_data}. Retrying.")
                        else:
                            logger.info(f"Successful response on attempt {attempt}.")
                        return response_json
                
                elif 500 <= status < 600:
                    logger.error(f"Server error {status} {reason}")
                    # Continue to retry
                
                else:
                    try:
                        response.raise_for_status()
                    except requests.HTTPError as exc:
                        logger.error(f"Client error {status}: {exc}")
                        raise  # Raise exception, no retry for client errors
            
            # Retry with backoff
            sleeptime = backoff * (2 ** (attempt - 1))
            logger.info(f"Sleeping {sleeptime:.1f} seconds before next attempt.")
            time.sleep(sleeptime)

        raise RuntimeError(f"Exceeded max attempts ({max_attempts}) for parameters={api_data}")