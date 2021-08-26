# -*- coding: utf-8 -*-
"""
@Time    : 9/21/20 1:10 PM
@Author  : Lucky
@Email   : lucky_soft@163.com
@File    : pcd.py
@Desc    : Description about this file
"""
from fastapi import APIRouter, HTTPException
from typing import List

from app.api.models import ShowLabel, ProjectIn
from app.api import db_manager

pcd = APIRouter()

@pcd.get('/list', response_model=List[ShowLabel])
async def get_pcd():
    pcd_label = await db_manager.get_labels()
    #pcd_label = db_manager.get_labels()
    if not pcd_label:
        raise HTTPException(status_code=404, detail="Label not found")
    return pcd_label

@pcd.post('/', response_model=ShowLabel, status_code = 201)
async def create_project(payload: ProjectIn):
    project_id = await db_manager.create_projects(payload)
    response = {
        'id': project_id,
        **payload.dict()
    }
    return response
