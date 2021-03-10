from sqlalchemy.ext.declarative import declarative_base


class Model(declarative_base()):
    __abstract__ = True

    class ModelNotFound(Exception):
        pass
