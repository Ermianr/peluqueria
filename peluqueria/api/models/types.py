from datetime import datetime
from typing import Annotated

import pendulum
from pydantic import PlainSerializer, StringConstraints

from peluqueria.constants import PHONE_REGEX


def format_date(dt_standard: datetime) -> str:
    pendulum_dt = pendulum.instance(dt_standard)
    dt_colombia = pendulum_dt.in_timezone("America/Bogota")
    day_name = dt_colombia.format("dddd", locale="es").capitalize()
    day_number = dt_colombia.day
    month = dt_colombia.format("MMM", locale="es").capitalize().lower()
    hour = dt_colombia.format("h:mmA").lower()
    return f"{day_name}, {day_number} de {month} {hour}"


Name = Annotated[str, StringConstraints(strip_whitespace=True)]
Phone = Annotated[str, StringConstraints(pattern=PHONE_REGEX)]
DateCo = Annotated[
    datetime,
    PlainSerializer(format_date, return_type="str"),
]
# ObjectIdStr = Annotated[str, Field(alias="_id")]
