from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, model_validator

# enum
class Priority(str, Enum):
    DEFAULT = "default"
    URGENT = "urgent"


class VehicleType(str, Enum):
    CAR = "car"
    ON_FOOT = "on_foot"
    BICYCLE = "bicycle"
    PUBLIC_TRANSPORT = "public_transport"

class Skill(str, Enum):
    CONNECTION_CLIENT = "connection_client"
    ACCIDENTS_ON_TKD = "accidents_on_tkd"
    ADD_EQUIPMENT_ORDER = "add_equipment_order"
    LOCAL_APPLICATION = "local_application"
class Equipment(str, Enum):
    pass


class Location(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    address: Optional[str] = None


class Duration(list, Enum):
    # время в пути + время работы + время на документы
    CONNECTION_CLIENT_T = [20, 60, 10]
    ACCIDENTS_ON_TKD_T = [20, 80,  0]
    ADD_EQUIPMENT_ORDER_T = [20, 10, 10]
    LOCAL_APPLICATION_T = [20, 30, 0]


# pydantic schemas
class Request(BaseModel):
    id: int
    location: Location
    priority: Priority

    required_skill: Skill
    required_equipment: Optional[Equipment] = None

    time_window_start: datetime
    time_window_end: datetime

    duration: Duration

    @model_validator(mode="after")
    def validate_time_window(self):
        if self.time_window_start >= self.time_window_end:
            raise ValueError(
                "time_window_start must be before time_window_end"
            )

        return self


class Engineer(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=150)

    start_location: Location

    shift_start: datetime
    shift_end: datetime

    skills: list[Skill] = Field(
        min_length=1,
        max_length=3,
    )

    vehicle_type: VehicleType

    @model_validator(mode="after")
    def validate_engineer(self):
        if self.shift_start >= self.shift_end:
            raise ValueError(
                "shift_start must be before shift_end"
            )

        if len(set(self.skills)) != len(self.skills):
            raise ValueError(
                "Engineer skills must be unique"
            )

        return self