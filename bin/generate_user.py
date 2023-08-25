from argparse import ArgumentParser

from app.models import User
from app.views.depends import SessionType
from db.sessions import SessionLocal


parser = ArgumentParser()
parser.add_argument('--name', type=str, required=True)
parser.add_argument('--password', type=str, required=True)
args = parser.parse_args()


session: SessionType = SessionLocal()
try:
    user = User()
    user.username = args.name
    user.password = args.password
    session.add(user)
    session.commit()
except Exception as e:
    session.rollback()
    raise e
finally:
    session.close()
