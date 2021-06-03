import logging
from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status

from .depends import get_session, SessionType
from app import schemas, auth
from app.service.report import ReportManager


logger = logging.getLogger(__name__)
api = APIRouter(prefix='/report', tags=['API'])


@api.post('', response_model=schemas.Report)
def rebate_report(
    report_parameters: Union[schemas.RebateReportParameters, schemas.PairsVolumeReportParameters],
    session: SessionType = Depends(get_session),
    user: schemas.UserDB = Depends(auth.get_current_active_user)
) -> schemas.Report:
    try:
        return ReportManager(report_parameters, session).get_report()
    except ReportManager.QueryFileException as ex:
        logger.exception(ex)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='report_name error')
