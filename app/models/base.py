from typing import Iterable, Optional

from sqlalchemy.ext.declarative import declarative_base


class Model(declarative_base()):
    __abstract__ = True

    class ModelNotFound(Exception):
        pass

    def to_dict(self, exclude: Optional[Iterable] = None):
        if not exclude:
            exclude = set()
        else:
            exclude = set(exclude)

        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in exclude
        }

    def to_tuple(self, exclude: Optional[Iterable] = None):
        if not exclude:
            exclude = set()
        else:
            exclude = set(exclude)

        return tuple(
            getattr(self, column.name)
            for column in self.__table__.columns
            if column.name not in exclude
        )

    def get_column_names(self, exclude: Optional[Iterable] = None):
        if not exclude:
            exclude = set()
        else:
            exclude = set(exclude)

        return tuple(
            column.name
            for column in self.__table__.columns
            if column.name not in exclude
        )
