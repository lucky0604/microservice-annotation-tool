# -*- coding: utf-8 -*-
"""
@Time    : 9/21/20 1:08 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : db_manager.py
@Desc    : Description about this file
"""
from app.api.models import ShowLabel, ProjectIn
from app.api.db import project, database

async def get_labels():
    query = project.select()
    return await database.fetch_all(query=query)

async def create_projects(payload: ProjectIn):
    query = project.insert().values(**payload.dict())
    return await database.execute(query = query)
