from datetime import datetime

from pydantic import BaseModel


class KalmanLogEntry(BaseModel):
    timestamp: datetime
    price_forex: float
    price_crypto: float
    ts_data: int
    s1_x: float
    s1_P: float
    s2_x: float
    s2_P: float
    s3_x: float
    s3_P: float

    class Config:
        schema_extra = {
            'example': {
                'timestamp': datetime.utcnow(),
                'price_forex': 25.5,
                'price_crypto': 25.3,
                'ts_data': 124521515555,
                'ask': 1245.3,
                'price_fair': 1245.45,
                's1_x': 0.35,
                's1_P': 0.45,
                's2_x': 0.35,
                's2_P': 0.55,
                's3_x': 0.26,
                's3_P': 0.35,
            }
        }
