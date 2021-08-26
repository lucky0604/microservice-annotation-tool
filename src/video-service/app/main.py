#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from fastapi import FastAPI
from app.api.video_annotate import video_annotate
from app.api.db import metadata, database, engine
from app.utils.redisUtils import get_redis_pool
from starlette.middleware.cors import CORSMiddleware

metadata.create_all(engine)

app = FastAPI(openapi_url = '/api/v1/video/openapi.json', docs_url = '/api/v1/video/docs')

#####################################
# fix cors
####################################
'''
origins = [
    'http://localhost',
    'http://localhost:3000',
    'http://localhost:8002'
]
'''
origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.on_event('startup')
async def startup():
    app.state.redis = await get_redis_pool()
    await database.connect()

@app.on_event('shutdown')
async def shutdown():
    app.state.redis.close()
    await app.state.redis.wait_closed()
    await database.disconnect()

app.include_router(video_annotate, prefix = '/api/v1/video', tags = ['video'])
