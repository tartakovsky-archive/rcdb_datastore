import sentry_sdk
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


def init_sentry(dsn):
    if dsn:
        sentry_sdk.init(
            dsn=dsn,
            integrations=[
                SqlalchemyIntegration()
            ],
            traces_sample_rate=0.
        )
        print('Sentry enabled', dsn)
    else:
        print('Sentry disabled')
