from datetime import datetime

from pydantic import BaseModel, condecimal, constr

from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class TradeLog(BaseModel):
    timestamp: datetime
    ts_end: datetime
    channel: constr(max_length=500)
    swap_id: int

    class Config(CustomJSONEncoderMixin):
        pass
