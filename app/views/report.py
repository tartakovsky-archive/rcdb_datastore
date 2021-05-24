import logging
from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy import text

from .depends import get_session, SessionType
from app import schemas, auth


logger = logging.getLogger(__name__)


api = APIRouter(prefix='/report', tags=['API'])
QUERY = open('app/views/rebate_report.sql').read()


@api.post('/rebate', response_model=Optional[schemas.RebateReport])
def rebate_report(
    report_parameters: schemas.RebateReportParameters,
    session: SessionType = Depends(get_session),
    user: schemas.UserDB = Depends(auth.get_current_active_user)
) -> schemas.RebateReport:
    result = session.execute(text(QUERY), report_parameters.alchemy_context)
    headers = [name[len('report_'):] if name.startswith('report_') else name for name, *_ in result.cursor.description]
    return schemas.RebateReport(__root__=[
        dict(zip(headers, row)) for row in result
    ])
