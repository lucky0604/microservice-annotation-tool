# -*- coding: utf-8 -*-
"""
@Time    : 9/21/20 12:52 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : main.py
@Desc    : Description about this file
"""
from fastapi import FastAPI
from app.api.pcd import pcd
from app.api.db import metadata, database, engine

metadata.create_all(engine)

app = FastAPI(openapi_url="/api/v1/pcd/openapi.json", docs_url="/api/v1/pcd/docs")

@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

app.include_router(pcd, prefix='/api/v1/pcd', tags=['pcd'])
