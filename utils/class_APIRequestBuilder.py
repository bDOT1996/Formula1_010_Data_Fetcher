from abc import ABC, abstractmethod
from typing import Dict, Any

class APIRequestBuilder(ABC):
    @abstractmethod
    def build_payload(self, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def get_schema(self):
        pass

###############################################
### - Tier 1 - ################################
###############################################

class MeetingsRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'year', 'meeting_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "year": "Int64",
            "meeting_key": "Int64",
            "circuit_key": "Int64",
            "circuit_short_name": "string",
            "country_code": "string",
            "country_key": "Int64",
            "country_name": "string",
            "date_start": "datetime64[ns, UTC]",
            "gmt_offset": "string",
            "location": "string",
            "meeting_code": "string",
            "meeting_key": "Int64",
            "meeting_name": "string",
            "meeting_official_name": "string"
        }


###############################################
### - Tier 2 - ################################
###############################################

class SessionsRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'year', 'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "year": "Int64",
            "meeting_key": "Int64",
            "session_key": "Int64",
            "circuit_key": "Int64",
            "circuit_short_name": "string",
            "country_code": "string",
            "country_key": "Int64",
            "country_name": "string",
            "date_end": "datetime64[ns, UTC]",
            "date_start": "datetime64[ns, UTC]",
            "gmt_offset": "string",
            "location": "string",
            "session_name": "string",
            "session_type": "string"
        }


###############################################
### - Tier 3 - ################################
###############################################

class DriversRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "driver_number": "Int64",
            "broadcast_name": "string",
            "country_code": "string",
            "first_name": "string",
            "full_name": "string",
            "headshot_url": "string",
            "last_name": "string",
            "name_acronym": "string",
            "team_colour": "string",
            "team_name": "string"
        }

class RaceControlRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "date": "datetime64[ns, UTC]",
            "category": "string",
            "driver_number": "Int64",
            "flag": "string",
            "lap_number": "Int64",
            "meeting_key": "Int64",
            "message": "string",
            "scope": "string",
            "sector": "Int64"
        }

class SessionResultRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "driver_number": "Int64",
    
            "dnf": "boolean",
            "dns": "boolean",
            "dsq": "boolean",
            
            "duration": "object",
            "gap_to_leader": "object",
            
            "number_of_laps": "Int64",
            "position": "Int64"
            
        }

class StartingGridRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "driver_number": "Int64",
            "grid_position": "Int64",
            "lap_duration": "float64",
            "position": "Int64"
        }

class StintsRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "driver_number": "Int64",
            "compound": "string",
            "driver_number": "Int64",
            "lap_end": "Int64",
            "lap_start": "Int64",
            "meeting_key": "Int64",
            "session_key": "Int64",
            "stint_number": "Int64",
            "tyre_age_at_start": "Int64"
        }

class TeamRadioRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "session_key": "Int64",
            "meeting_key": "Int64",
            "driver_number": "Int64",
            "date": "datetime64[ns, UTC]",
            "message": "string"
        }

class WeatherRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "date": "datetime64[ns, UTC]",
            "air_temperature": "float64",
            "track_temperature": "float64",
            "humidity": "float64",
            "pressure": "float64",
            "rainfall": "float64",
            "wind_speed": "float64",
            "wind_direction": "float64"
        }


###############################################
### - Tier 4 - ################################
###############################################

class LapsRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key','driver_number'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "session_key": "Int64",
            "driver_number": "Int64",
            "meeting_key": "Int64",
            "lap_number": "Int64",
            "date_start": "datetime64[ns, UTC]",
            "duration_sector_1": "float64",
            "duration_sector_2": "float64",
            "duration_sector_3": "float64",
            "i1_speed": "Int64",
            "i2_speed": "Int64",
            "is_pit_out_lap": "boolean",
            "lap_duration": "float64",
            "segments_sector_1": "object",
            "segments_sector_2": "object",
            "segments_sector_3": "object",
            "st_speed": "Int64",
        }

class OvertakesRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        if 'driver_number' in params:
            result['overtaking_driver_number'] = params['driver_number']
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "date": "datetime64[ns, UTC]",
            "overtaking_driver_number": "Int64",
            "overtaken_driver_number": "Int64",
            "position": "Int64"
        }

class PitRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key','driver_number'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "driver_number": "Int64",
            "date": "datetime64[ns, UTC]",
            "lap_number": "Int64",
            "pit_duration": "float64"
            
        }

class PositionRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key','driver_number'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "driver_number": "Int64",
            "date": "datetime64[ns, UTC]",
            "position": "Int64"
        }


###############################################
### - Tier 5.1 - ##############################
###############################################

class IntervalsRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        if 'date_start' in params:
            result['date>'] = params['date_start']
        if 'date_end' in params:
            result['date<'] = params['date_end']
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "driver_number": "Int64",
            "date": "datetime64[ns, UTC]",
            #"gap_to_leader": "float64",
            "gap_to_leader": "string",
            "interval": "float64"
        }

###############################################
### - Tier 5.2 - ##############################
###############################################

class CarDataRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        if 'date_start' in params:
            result['date>'] = params['date_start']
        if 'date_end' in params:
            result['date<'] = params['date_end']
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "driver_number": "Int64",
            "date": "datetime64[ns, UTC]",
            "brake": "Int64",
            "drs": "Int64",
            "n_gear": "Int64",
            "rpm": "Int64",
            "speed": "Int64",
            "throttle": "Int64"
        }

class LocationRequestBuilder(APIRequestBuilder):
    def build_payload(self, params: Dict[str,Any]):
        allowed_keys = {'meeting_key', 'session_key'}
        result = {k: v for k, v in params.items() if k in allowed_keys}
        if 'date_start' in params:
            result['date>'] = params['date_start']
        if 'date_end' in params:
            result['date<'] = params['date_end']
        return result

    def get_schema(self):
        return {
            "meeting_key": "Int64",
            "session_key": "Int64",
            "driver_number": "Int64",
            "date": "datetime64[ns, UTC]",
            "x": "float64",
            "y": "float64",
            "z": "float64"
        }