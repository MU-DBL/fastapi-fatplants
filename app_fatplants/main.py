from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from db import models,database,schemas,crud
from db.database import database_conn_obj

from router_imports import routers
import os

import logging
from logging_config import setup_logging

# models.Base.metadata.create_all(bind=engine)  #Creating db session engine

# Configure logging
setup_logging()

app = FastAPI(
    title="FastAPI",
    description="Not Tested",
    version="1.0",
    prefix="/api"
)

sleep_time = 10

@app.on_event("startup")
async def startup():
    logging.info("fatplants_app is starting up...")
    await database_conn_obj.connect()

@app.on_event("shutdown")
async def shutdown():
    logging.info("fatplants_app is shutting down...")
    await database_conn_obj.disconnect()

# environment specific origins taken from environment variable
allow_origins = os.environ.get("CORS_ALLOW_ORIGINS", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[allow_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Dependency for db connection
# def get_db():
#     dbc = SessionLocal()
#     try:
#         yield dbc
#     finally:
#         dbc.close()

@app.get('/')
def index():
    return {'message':'Welcome to fatplants FastAPI Homepage. Please enter any valid endpoint'}

for route in routers:
    app.include_router(route.router)

