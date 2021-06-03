import os

import sqlalchemy as sa

from app import schemas
from app.views.depends import SessionType

QUERIES_DIR = 'queries'


class ReportManager:
    class QueryFileException(BaseException):
        pass

    def __init__(self, report_parameters: schemas.ReportParameters, session: SessionType):
        self.report_parameters: schemas.ReportParameters = report_parameters
        self.session = session

    def _get_query_text(self) -> sa.text:
        path = os.path.join(QUERIES_DIR, f'{self.report_parameters.report_name}.sql')
        if os.path.exists(path) and os.path.isfile(path):
            with open(path) as file:
                return sa.text(file.read())
        raise self.QueryFileException(
            f'path `{path}` is exists: {os.path.exists(path)} is file: {os.path.isfile(path)}')

    def get_report(self) -> schemas.Report:
        query_text = self._get_query_text()
        alchemy_context = self.report_parameters.get_alchemy_context()

        result = self.session.execute(query_text, alchemy_context)
        report_prefix = 'report_'
        headers = [
            name[len(report_prefix):] if name.startswith(report_prefix) else name
            for name, *_ in result.cursor.description
        ]
        return schemas.Report(__root__=[
            dict(zip(headers, row)) for row in result
        ])
