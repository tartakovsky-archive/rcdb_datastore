from datetime import datetime

from pydantic import BaseModel, condecimal, constr

from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class Orderbook(BaseModel):
    timestamp: datetime
    ts_l: datetime
    channel: constr(max_length=500)
    b: decimal_type
    a: decimal_type
    b_a: decimal_type
    a_a: decimal_type

    class Config(CustomJSONEncoderMixin):
        pass
