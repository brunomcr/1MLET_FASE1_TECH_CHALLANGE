import uvicorn
from fastapi import FastAPI

from .api.routers import *
from .dependencies import injector
from .domain.interfaces.services import DBPopulatorService
# from .helpers import async_get_data

# print("Scrapping Embrapa Website Data")
# async_get_data()

print("Populating the database")
db_populator_service = injector.get(DBPopulatorService)
db_populator_service.populate()

print("Starting the application")
app = FastAPI()
app.include_router(export_router)
app.include_router(import_router)
app.include_router(processing_router)
app.include_router(production_router)
app.include_router(trading_router)
app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
