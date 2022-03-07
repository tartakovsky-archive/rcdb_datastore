from datetime import datetime

from pydantic import BaseModel, condecimal, constr as standard_constr

from .mixins import CustomJSONEncoderMixin

decimal_type = condecimal(max_digits=27, decimal_places=18)


class UnclaimedBNB(BaseModel):
    timestamp: datetime
    name: standard_constr(min_length=1, max_length=200)
    unclaimed: decimal_type

    class Config(CustomJSONEncoderMixin):
        pass
