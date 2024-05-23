from fastapi import APIRouter, HTTPException, Security
import logging

from ..di import injector
from ...domain.interfaces.services import TradingDataService
from ...domain.responses import GetTradingDataByYearResponse
from ...services import JWTBearer

logging.basicConfig(level=logging.INFO)

trading_data_service = injector.get(TradingDataService)
trading_router = APIRouter()


@trading_router.get("/trading/{year}",
                    response_model=GetTradingDataByYearResponse,
                    dependencies=[Security(JWTBearer())])
async def get_trading_data_by_year(year: int) -> GetTradingDataByYearResponse:
    try:
        return await trading_data_service.get_trading_data_by_year(year)
    except Exception as e:
        logging.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))