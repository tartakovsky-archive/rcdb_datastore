from datetime import datetime

from pydantic import BaseModel, condecimal, constr

from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class Ticker(BaseModel):
    timestamp: datetime
    channel: constr(max_length=500)
    p: decimal_type
    q: decimal_type
    bm: bool

    class Config(CustomJSONEncoderMixin):
        pass
