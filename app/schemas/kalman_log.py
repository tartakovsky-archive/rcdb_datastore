from datetime import datetime

from pydantic import BaseModel, condecimal, constr

from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class KalmanLog(BaseModel):
    timestamp: datetime
    channel: constr(max_length=500)
    brt: decimal_type
    art: decimal_type

    class Config(CustomJSONEncoderMixin):
        pass
